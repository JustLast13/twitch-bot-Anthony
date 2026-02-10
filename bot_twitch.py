from twitchio.ext import commands
import random
import asyncio
import os
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Configuración
MESSAGE_INTERVAL = 60  # Intervalo de tiempo entre mensajes en segundos (1 minuto)
MESSAGES = [
    "Hola, bienvenid@ pasale.",
    "Que guapa está la streamer.",
    "Me estoy aburriendo, perdón.",
    "Hoy sí que hizo frío, ¿no?",
    "Qué calor hizo hoy.",
    "Mmm, necesito aprender a dibujar, ¿no sé?"
]

class TwitchBot(commands.Bot):
    def __init__(self):
        # Obtener credenciales de variables de entorno
        token = os.getenv('TWITCH_TOKEN')
        client_id = os.getenv('TWITCH_CLIENT_ID')
        bot_name = os.getenv('TWITCH_BOT_NAME', 'Anthony_love')
        
        if not token:
            logger.error("❌ ERROR: TWITCH_TOKEN no está configurado")
            logger.error("⚠️  Ve a GitHub → Settings → Secrets → New repository secret")
            logger.error("⚠️  Agrega: TWITCH_TOKEN = oauth:tu_token_real")
            raise ValueError("TWITCH_TOKEN no configurado")
        
        if not client_id:
            logger.error("❌ ERROR: TWITCH_CLIENT_ID no está configurado")
            logger.error("⚠️  Ve a GitHub → Settings → Secrets → New repository secret")
            logger.error("⚠️  Agrega: TWITCH_CLIENT_ID = tu_client_id_real")
            raise ValueError("TWITCH_CLIENT_ID no configurado")
        
        logger.info(f"✅ Token encontrado: {token[:15]}...")
        logger.info(f"✅ Client ID encontrado: {client_id[:10]}...")
        logger.info(f"✅ Nombre del bot: {bot_name}")
        
        super().__init__(
            token=token,
            client_id=client_id,
            nick=bot_name,
            prefix='!',
            initial_channels=['arisuhz', 'justlast13']
        )
        
        self.keep_running = True
        logger.info("🤖 Bot inicializado correctamente")

    async def event_ready(self):
        """Evento cuando el bot se conecta exitosamente"""
        logger.info(f'✅ Bot {self.nick} conectado a Twitch')
        logger.info(f'📺 Canales conectados: {[c.name for c in self.connected_channels]}')
        
        # Iniciar tarea de mensajes periódicos
        asyncio.create_task(self.enviar_mensajes_periodicos())
        logger.info("🔄 Tarea de mensajes periódicos iniciada")

    async def event_message(self, message):
        """Procesa todos los mensajes recibidos"""
        if message.echo:
            return
        
        logger.info(f'#{message.channel.name} - {message.author.name}: {message.content}')
        await self.handle_commands(message)

    async def event_command_error(self, ctx, error):
        """Maneja errores de comandos"""
        logger.error(f"❌ Error en comando {ctx.command.name}: {error}")
        await ctx.send(f"❌ Ocurrió un error: {str(error)[:100]}")

    async def enviar_mensajes_periodicos(self):
        """Envía mensajes automáticos periódicamente"""
        await self.wait_for_ready()  # Esperar a que el bot esté listo
        
        logger.info(f"⏰ Mensajes automáticos configurados cada {MESSAGE_INTERVAL} segundos")
        
        while self.keep_running:
            try:
                for channel in self.connected_channels:
                    if channel and hasattr(channel, 'send'):
                        message = random.choice(MESSAGES)
                        await channel.send(message)
                        logger.info(f"📨 Mensaje automático a {channel.name}: {message}")
                
                await asyncio.sleep(MESSAGE_INTERVAL)
                
            except Exception as e:
                logger.error(f"❌ Error en mensajes periódicos: {e}")
                await asyncio.sleep(30)  # Esperar antes de reintentar

    @commands.command(name='anthony')
    async def anthony(self, ctx):
        """Comando principal !anthony"""
        content = ctx.message.content.lower()
        author = ctx.author.name
        
        logger.info(f"🎮 Comando !anthony de {author}: {content}")
        
        # Respuestas específicas
        respuestas_especificas = {
            "quién es tu streamer favorito": "Obviamente Arisuhz o también llamada Juana.",
            "cuál es tu color favorito": "El amarillo, pero prefiero el celeste.",
            "tienes una relación actualmente": "Sí, pero ella no lo sabe.",
            "quién te programó": "No soy un bot, yo sí existo. ¡Saludos!",
            "tienes juego favorito": "Juego mucho, pero no sabría decirte cuál es mi favorito.",
            "conoces a kody": "Sí, es gracioso, es un naco y un estúpido, pero igual me agrada. Saludos.",
            "ves anime": "Sí, veo mucho, pero soy fan de My Hero Academia y Jujutsu Kaisen. Aunque no estoy al día, estoy esperando a una personita para terminarlo.",
            "conoces a emakonda": "Sí, es un streamer muy chido, solo que le gusta K-On. También lo veo, no me juzguen.",
            "sabes quien es el culon del canal?": "Según recuerdo que Justlast y Cubic aunque cubic es más de preguntarte si cortarte el pie o estar en las alcantarillas (Que agradable sujeto)"
        }
        
        for pregunta, respuesta in respuestas_especificas.items():
            if pregunta in content:
                logger.info(f"✅ Respondiendo pregunta específica: {pregunta}")
                await ctx.send(respuesta)
                return
        
        # Respuesta aleatoria si no es pregunta específica
        responses = [
            f"¡Ey {author}, qué guap@ estás!💐",
            f"¡{author}, ten un bonito día!☀️🌹",
            f"¿{author}, quieres un abrazo, reina? arisuh1PATITO",
            f"¡{author}, eres increíble!😎",
            f"¡{author}, hoy será un gran día!✨",
            f"{author}, recuerda, nunca tendrás un mal día si estoy contigo.",
            f"{author}, ahorita no, estoy enojado contigo.",
            f"{author}, NO MOLESTE.",
            f"{author}, tú eres todo lo que necesito.",
            f"{author}, hay Kody, como me haces reír con tus payasadas, eres un naco y un estúpido.",
            f"{author}, como que hace calor, ¿no? Porque me derrito con tus ojos.",
            f"{author}, tengo sed, ¿tú no quieres agua?",
            f"{author}, estoy aburrido, ¿no quieres jugar algo?",
            f"{author}, tengo frío.",
            f"{author}, soporta mana 💅.",
            f"{author}, no sé hermano, te la debo. Saludos.",
            f"{author}, buenas a todos y un beso a la streamer.",
            f"{author}, feliz año 2025, abrazos a todos y un beso a la streamer🤭",
            f"{author}, te invito a ver SAO. VAS? 😋"
        ]
        
        response = random.choice(responses)
        logger.info(f"🎲 Respuesta aleatoria para {author}")
        await ctx.send(response)

    @commands.command(name='hola')
    async def hola(self, ctx):
        """Comando simple de saludo"""
        await ctx.send(f'¡Hola {ctx.author.name}! 👋')
        logger.info(f"👋 Saludo para {ctx.author.name}")

    @commands.command(name='comandos')
    async def comandos(self, ctx):
        """Muestra los comandos disponibles"""
        comandos_lista = "!anthony - Interactúa con Anthony | !hola - Saludo simple | !comandos - Esta ayuda"
        await ctx.send(f"📋 Comandos disponibles: {comandos_lista}")
        logger.info(f"📋 Mostrando comandos a {ctx.author.name}")

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Verifica si el bot está vivo"""
        await ctx.send(f'🏓 ¡Pong! {ctx.author.name}, el bot está vivo y en GitHub Codespaces!')
        logger.info(f"🏓 Ping de {ctx.author.name}")

    async def close(self):
        """Cierra el bot correctamente"""
        self.keep_running = False
        await super().close()
        logger.info("🛑 Bot cerrado correctamente")

def main():
    """Función principal para iniciar el bot"""
    logger.info("=" * 50)
    logger.info("🚀 INICIANDO BOT DE TWITCH EN GITHUB CODESPACES")
    logger.info("=" * 50)
    
    try:
        bot = TwitchBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("🛑 Bot detenido por el usuario (Ctrl+C)")
    except Exception as e:
        logger.error(f"❌ ERROR FATAL: {e}")
        logger.error("💡 Posibles soluciones:")
        logger.error("1. Verifica que TWITCH_TOKEN y TWITCH_CLIENT_ID estén en GitHub Secrets")
        logger.error("2. Asegúrate de que el token no haya expirado")
        logger.error("3. Revisa que los canales existan")
        raise

if __name__ == "__main__":
    main()
