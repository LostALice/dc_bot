#Code by AkinoAlice@Tyrant_Rex

from core.classes import Cog_extension
from discord.ext import commands
from requests import get
from discord import File
from io import BytesIO
from PIL import Image

class Tools(Cog_extension):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.command(aliases=["PDF","pdf"], help="""Convert image to PDF""")
    async def to_PDF(self, ctx: commands.Context) -> None:
        self.message_attachments = [i.url for i in ctx.message.attachments]
        image_byte_list: list[Image.Image] = []

        for i in self.message_attachments:
            image_byte_list.append(Image.open(BytesIO(get(i).content)))

        byte = BytesIO()
        image_byte_list[0].save(byte, format="pdf", save_all=True, append_images=image_byte_list[1:])
        byte.seek(0)
        pdf_file: File = File(byte, filename="Doc.pdf")
        await ctx.send(file=pdf_file)
        await ctx.message.delete()

async def setup(client: commands.Bot):
    await client.add_cog(Tools(client))