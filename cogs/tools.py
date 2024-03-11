#Code by AkinoAlice@Tyrant_Rex

from PIL import Image
from io import BytesIO
from requests import get
from discord.ext import commands

class Tools(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.command(aliases=["pdf"], help="""Turn image to PDF""")
    async def to_PDF(self, ctx: commands.Context) -> None:
        self.message_attachments = [i.url for i in ctx.message.attachments]
        image_byte_list: list[bytes] = []
        for i in self.message_attachments:
            image_byte_list.append(Image.open(BytesIO(get(i).content)))
        print(image_byte_list)

async def setup(client):
    await client.add_cog(Tools(client))