import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from app.services.base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)

class WebScraper(BaseScraper):
    """Generic web scraper for shelter websites"""
    
    async def fetch_dogs(self) -> List[Dict[str, Any]]:
        """Fetch dogs using web scraping"""
        
        if not self.shelter.scraping_config:
            raise ValueError("No scraping configuration found for this shelter")
        
        config = self.shelter.scraping_config
        
        async with aiohttp.ClientSession() as session:
            dogs_data = []
            
            # Get list of dog URLs
            dog_urls = await self._get_dog_urls(session, config)
            
            # Scrape each dog's details
            for url in dog_urls:
                try:
                    dog_data = await self._scrape_dog_details(session, url, config)
                    if dog_data:
                        dogs_data.append(dog_data)
                except Exception as e:
                    logger.warning(f"Failed to scrape dog from {url}: {str(e)}")
                    continue
            
            return dogs_data
    
    async def _get_dog_urls(self, session: aiohttp.ClientSession, config: Dict[str, Any]) -> List[str]:
        """Get list of dog profile URLs"""
        
        base_url = self.shelter.website_url
        listing_url = config.get('listing_url', base_url)
        
        try:
            async with session.get(listing_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch listing page: {response.status}")
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract dog URLs using CSS selector
                url_selector = config.get('dog_url_selector')
                if not url_selector:
                    raise ValueError("No dog_url_selector in scraping config")
                
                links = soup.select(url_selector)
                urls = []
                
                for link in links:
                    href = link.get('href')
                    if href:
                        # Convert relative URLs to absolute
                        if href.startswith('/'):
                            href = base_url.rstrip('/') + href
                        elif not href.startswith('http'):
                            href = base_url.rstrip('/') + '/' + href
                        urls.append(href)
                
                return urls
                
        except Exception as e:
            logger.error(f"Failed to get dog URLs from {listing_url}: {str(e)}")
            return []
    
    async def _scrape_dog_details(self, session: aiohttp.ClientSession, url: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Scrape details for a single dog"""
        
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch dog page: {response.status}")
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract dog data using selectors from config
                selectors = config.get('selectors', {})
                
                dog_data = {
                    'external_id': self._extract_id_from_url(url),
                    'original_url': url,
                    'name': self._extract_text(soup, selectors.get('name')),
                    'breed': self._extract_text(soup, selectors.get('breed')),
                    'age': self._extract_text(soup, selectors.get('age')),
                    'size': self._extract_text(soup, selectors.get('size')),
                    'gender': self._extract_text(soup, selectors.get('gender')),
                    'weight': self._extract_text(soup, selectors.get('weight')),
                    'description': self._extract_text(soup, selectors.get('description')),
                    'medical_info': self._extract_text(soup, selectors.get('medical_info')),
                    'behavior_notes': self._extract_text(soup, selectors.get('behavior_notes')),
                    'location': self._extract_text(soup, selectors.get('location')),
                    'photos': self._extract_photos(soup, selectors.get('photos'), url)
                }
                
                # Remove None values
                dog_data = {k: v for k, v in dog_data.items() if v is not None}
                
                return dog_data
                
        except Exception as e:
            logger.error(f"Failed to scrape dog details from {url}: {str(e)}")
            return None
    
    def _extract_text(self, soup: BeautifulSoup, selector: str) -> str:
        """Extract text using CSS selector"""
        if not selector:
            return None
            
        element = soup.select_one(selector)
        if element:
            return element.get_text(strip=True)
        
        return None
    
    def _extract_photos(self, soup: BeautifulSoup, selector: str, base_url: str) -> List[str]:
        """Extract photo URLs using CSS selector"""
        if not selector:
            return []
        
        photos = []
        elements = soup.select(selector)
        
        for element in elements:
            # Check for img src or data-src
            src = element.get('src') or element.get('data-src')
            if src:
                # Convert relative URLs to absolute
                if src.startswith('/'):
                    src = base_url.split('/')[0] + '//' + base_url.split('/')[2] + src
                elif not src.startswith('http'):
                    src = base_url.rstrip('/') + '/' + src
                photos.append(src)
        
        return photos
    
    def _extract_id_from_url(self, url: str) -> str:
        """Extract unique ID from URL"""
        # Try to extract ID from URL patterns
        import re
        
        # Look for common ID patterns
        patterns = [
            r'/(\d+)/?$',  # ID at end of URL
            r'id=(\d+)',   # ID as query parameter
            r'/([^/]+)/?$'  # Last path segment
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # Fallback: use the full URL as ID
        return url.split('/')[-1] or url.split('/')[-2]
