import asyncio
import os
from .protocol import *

class FileTransferClient:
    def __init__(self, host, port=DEFAULT_PORT):
        self.host = host
        self.port = port

    async def send_file(self, filepath, progress_callback=None):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        file_name = os.path.basename(filepath)
        file_size = os.path.getsize(filepath)

        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(self.host, self.port),
            timeout=10
        )

        try:
            request = create_message({
                "type": "file_transfer_request",
                "file_name": file_name,
                "file_size": file_size
            })
            writer.write(request)
            await writer.drain()

            response = await asyncio.wait_for(read_message(reader), timeout=30)

            if not response.get('accepted'):
                raise Exception(response.get('message', 'Transfer rejected'))

            sent = 0
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    writer.write(chunk)
                    await writer.drain()
                    sent += len(chunk)

                    if progress_callback:
                        progress_callback(sent, file_size)

            complete = await asyncio.wait_for(read_message(reader), timeout=30)

            if complete.get('status') != 'ok':
                raise Exception("Server did not confirm file receipt")

            return True

        finally:
            writer.close()
            await writer.wait_closed()

    async def ping(self):
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port),
                timeout=5
            )
            writer.write(create_message({"type": "ping"}))
            await writer.drain()
            response = await asyncio.wait_for(read_message(reader), timeout=5)
            writer.close()
            await writer.wait_closed()
            return response.get('type') == 'pong'
        except:
            return False