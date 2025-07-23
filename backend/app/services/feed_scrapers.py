from typing import List, Dict, Any
from app.services.base_scraper import BaseScraper
import aiohttp
import asyncio
import feedparser
import logging

logger = logging.getLogger(__name__)

class RSSFeedScraper(BaseScraper):
    """RSS feed scraper for shelters that provide RSS feeds"""
    
    async def fetch_dogs(self) -> List[Dict[str, Any]]:
        """Fetch dogs from RSS feed"""
        
        if not self.shelter.rss_feed_url:
            raise ValueError("No RSS feed URL configured for this shelter")
        
        try:
            # Parse RSS feed
            feed = feedparser.parse(self.shelter.rss_feed_url)
            
            if feed.bozo:
                raise ValueError(f"Invalid RSS feed: {feed.bozo_exception}")
            
            dogs_data = []
            
            for entry in feed.entries:
                try:
                    dog_data = self._parse_rss_entry(entry)
                    if dog_data:
                        dogs_data.append(dog_data)
                except Exception as e:
                    logger.warning(f"Failed to parse RSS entry: {str(e)}")
                    continue
            
            return dogs_data
            
        except Exception as e:
            logger.error(f"Failed to parse RSS feed from {self.shelter.rss_feed_url}: {str(e)}")
            return []
    
    def _parse_rss_entry(self, entry) -> Dict[str, Any]:
        """Parse a single RSS entry into dog data"""
        
        # Extract basic information
        dog_data = {
            'external_id': self._extract_id_from_entry(entry),
            'original_url': entry.get('link'),
            'name': entry.get('title', 'Unknown'),
            'description': self._clean_description(entry.get('summary', '')),
        }
        
        # Try to extract structured data from description or other fields
        content = entry.get('summary', '') + ' ' + entry.get('content', '')
        
        # Extract specific fields using patterns (this would need customization per RSS feed)
        dog_data.update(self._extract_structured_data(content))
        
        return dog_data
    
    def _extract_id_from_entry(self, entry) -> str:
        """Extract unique ID from RSS entry"""
        # Try guid first
        if hasattr(entry, 'guid'):
            return str(entry.guid)
        
        # Try to extract from link
        link = entry.get('link', '')
        if link:
            return link.split('/')[-1] or link.split('/')[-2]
        
        # Fallback to title hash
        return str(hash(entry.get('title', '')))
    
    def _clean_description(self, description: str) -> str:
        """Clean HTML from description"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(description, 'html.parser')
        return soup.get_text(strip=True)
    
    def _extract_structured_data(self, content: str) -> Dict[str, Any]:
        """Extract structured data from content using regex patterns"""
        import re
        
        data = {}
        
        # Common patterns for different fields
        patterns = {
            'breed': r'(?:raza|breed|tipo)[:]\s*([^\n]+)',
            'age': r'(?:edad|age|años|years|meses|months)[:]\s*([^\n]+)',
            'gender': r'(?:sexo|gender|género)[:]\s*([^\n]+)',
            'size': r'(?:tamaño|size)[:]\s*([^\n]+)',
            'weight': r'(?:peso|weight)[:]\s*([^\n]+)',
            'location': r'(?:ubicación|location|lugar)[:]\s*([^\n]+)',
        }
        
        for field, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                data[field] = match.group(1).strip()
        
        return data


class APIScraper(BaseScraper):
    """API-based scraper for shelters that provide APIs"""
    
    async def fetch_dogs(self) -> List[Dict[str, Any]]:
        """Fetch dogs from API"""
        
        if not self.shelter.api_endpoint:
            raise ValueError("No API endpoint configured for this shelter")
        
        config = self.shelter.api_config or {}
        headers = config.get('headers', {})
        auth = config.get('auth', {})
        
        try:
            async with aiohttp.ClientSession() as session:
                # Add authentication if configured
                if auth.get('type') == 'bearer':
                    headers['Authorization'] = f"Bearer {auth.get('token')}"
                elif auth.get('type') == 'api_key':
                    headers[auth.get('header', 'X-API-Key')] = auth.get('key')
                
                async with session.get(self.shelter.api_endpoint, headers=headers) as response:
                    if response.status != 200:
                        raise Exception(f"API request failed: {response.status}")
                    
                    data = await response.json()
                    
                    # Parse response based on API structure
                    dogs_data = self._parse_api_response(data, config)
                    
                    return dogs_data
                    
        except Exception as e:
            logger.error(f"Failed to fetch from API {self.shelter.api_endpoint}: {str(e)}")
            return []
    
    def _parse_api_response(self, data: Dict[str, Any], config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse API response into dog data"""
        
        dogs_data = []
        
        # Get the array of dogs from the response
        dogs_key = config.get('dogs_key', 'dogs')  # Key that contains the dogs array
        dogs_array = data.get(dogs_key, data)  # Default to root if no specific key
        
        if not isinstance(dogs_array, list):
            dogs_array = [dogs_array]  # Handle single dog response
        
        # Field mappings from API to our format
        field_mapping = config.get('field_mapping', {})
        
        for dog_item in dogs_array:
            dog_data = {
                'external_id': str(dog_item.get(field_mapping.get('id', 'id'), '')),
                'name': dog_item.get(field_mapping.get('name', 'name'), 'Unknown'),
                'breed': dog_item.get(field_mapping.get('breed', 'breed')),
                'age': dog_item.get(field_mapping.get('age', 'age')),
                'gender': dog_item.get(field_mapping.get('gender', 'gender')),
                'size': dog_item.get(field_mapping.get('size', 'size')),
                'weight': dog_item.get(field_mapping.get('weight', 'weight')),
                'description': dog_item.get(field_mapping.get('description', 'description')),
                'location': dog_item.get(field_mapping.get('location', 'location')),
                'original_url': dog_item.get(field_mapping.get('url', 'url')),
                'photos': self._extract_photos_from_api(dog_item, field_mapping)
            }
            
            # Remove None values
            dog_data = {k: v for k, v in dog_data.items() if v is not None}
            dogs_data.append(dog_data)
        
        return dogs_data
    
    def _extract_photos_from_api(self, dog_item: Dict[str, Any], field_mapping: Dict[str, Any]) -> List[str]:
        """Extract photo URLs from API response"""
        photos_field = field_mapping.get('photos', 'photos')
        photos = dog_item.get(photos_field, [])
        
        if isinstance(photos, str):
            return [photos]
        elif isinstance(photos, list):
            return [str(photo) for photo in photos if photo]
        
        return []
