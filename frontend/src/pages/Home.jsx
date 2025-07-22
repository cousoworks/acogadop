import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Heart, Search, Users, Award } from 'lucide-react'

const Home = () => {
  const stats = [
    { icon: Heart, label: 'Perros Acogidos', value: '150+' },
    { icon: Users, label: 'Familias Acogedoras', value: '80+' },
    { icon: Award, label: 'Adopciones Exitosas', value: '120+' },
    { icon: Search, label: 'Perros Disponibles', value: '25+' },
  ]

  const testimonials = [
    {
      name: 'María González',
      text: 'Acoger a Luna fue la mejor decisión. Ahora es parte de nuestra familia.',
      image: '👩‍🦰'
    },
    {
      name: 'Carlos Martín',
      text: 'El proceso fue muy fácil y el apoyo del equipo increíble.',
      image: '👨‍💼'
    },
    {
      name: 'Ana López',
      text: 'Gracias a FosterDogs encontré a mi compañero perfecto.',
      image: '👩‍💻'
    },
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-50 to-secondary-50 overflow-hidden">
        <div className="absolute inset-0 bg-white/20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="space-y-8"
            >
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-heading font-bold text-gray-900 leading-tight">
                <span className="text-primary-600">Acoge</span>,{' '}
                <span className="text-secondary-600">Ama</span>,{' '}
                <span className="text-primary-600">Adopta</span>
              </h1>
              
              <p className="text-xl text-gray-600 leading-relaxed max-w-xl">
                Dale una segunda oportunidad a un perro que lo necesita. 
                Conectamos corazones y creamos familias felices.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4">
                <Link
                  to="/dogs"
                  className="btn-primary text-lg px-8 py-3 inline-flex items-center justify-center"
                >
                  <Search className="w-5 h-5 mr-2" />
                  Ver Perros Disponibles
                </Link>
                <Link
                  to="/register"
                  className="btn-secondary text-lg px-8 py-3 inline-flex items-center justify-center"
                >
                  <Heart className="w-5 h-5 mr-2" />
                  Convertirse en Acogedor
                </Link>
              </div>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="relative"
            >
              <div className="relative z-10 bg-white rounded-2xl shadow-2xl p-8 transform rotate-3 hover:rotate-0 transition-transform duration-300">
                <div className="text-center space-y-4">
                  <div className="text-8xl animate-bounce-gentle">🐕</div>
                  <h3 className="text-2xl font-heading font-semibold text-gray-900">
                    ¡Encuentra tu compañero!
                  </h3>
                  <p className="text-gray-600">
                    Cada perro tiene una historia única y busca un hogar lleno de amor.
                  </p>
                </div>
              </div>
              <div className="absolute -top-4 -right-4 w-72 h-72 bg-primary-200 rounded-full blur-3xl opacity-30"></div>
              <div className="absolute -bottom-4 -left-4 w-72 h-72 bg-secondary-200 rounded-full blur-3xl opacity-30"></div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map(({ icon: Icon, label, value }, index) => (
              <motion.div
                key={label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="text-center space-y-4"
              >
                <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full">
                  <Icon className="w-8 h-8 text-primary-600" />
                </div>
                <div>
                  <div className="text-3xl font-bold text-gray-900">{value}</div>
                  <div className="text-gray-600 text-sm">{label}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-gray-900 mb-4">
              ¿Cómo Funciona?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Un proceso simple y transparente para conectar perros con familias acogedoras
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: '1',
                title: 'Regístrate',
                description: 'Crea tu perfil y cuéntanos sobre tu experiencia con perros.',
                icon: '📝'
              },
              {
                step: '2',
                title: 'Encuentra tu Match',
                description: 'Explora perros disponibles y encuentra el que conecte contigo.',
                icon: '❤️'
              },
              {
                step: '3',
                title: 'Acoge y Ama',
                description: 'Dale un hogar temporal y ayúdale a encontrar su familia definitiva.',
                icon: '🏠'
              }
            ].map(({ step, title, description, icon }, index) => (
              <motion.div
                key={step}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
                className="text-center space-y-6"
              >
                <div className="relative">
                  <div className="text-6xl mb-4">{icon}</div>
                  <div className="absolute -top-2 -right-2 w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                    {step}
                  </div>
                </div>
                <h3 className="text-xl font-heading font-semibold text-gray-900">
                  {title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-gray-900 mb-4">
              Historias de Éxito
            </h2>
            <p className="text-xl text-gray-600">
              Lo que dicen nuestras familias acogedoras
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={testimonial.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="card p-6 text-center space-y-4"
              >
                <div className="text-4xl">{testimonial.image}</div>
                <blockquote className="text-gray-600 italic">
                  "{testimonial.text}"
                </blockquote>
                <div className="font-medium text-gray-900">
                  {testimonial.name}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-primary-600 to-secondary-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="space-y-8"
          >
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-white">
              ¿Listo para Cambiar una Vida?
            </h2>
            <p className="text-xl text-white/90 max-w-2xl mx-auto">
              Únete a nuestra comunidad de familias acogedoras y ayuda a crear finales felices.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/dogs"
                className="bg-white text-primary-600 hover:bg-gray-100 font-medium py-3 px-8 rounded-lg transition-colors duration-200 inline-flex items-center justify-center"
              >
                <Search className="w-5 h-5 mr-2" />
                Explorar Perros
              </Link>
              <Link
                to="/register"
                className="border-2 border-white text-white hover:bg-white hover:text-primary-600 font-medium py-3 px-8 rounded-lg transition-all duration-200 inline-flex items-center justify-center"
              >
                <Heart className="w-5 h-5 mr-2" />
                Ser Acogedor
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default Home