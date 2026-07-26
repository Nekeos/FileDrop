import asyncio
import os
from .protocol import *

class FileTransferServer:
    def __init__(self, save_dir="received_files", host='0.0.0.0', port=DEFAULT_PORT):
        self.save_dir = save_dir
        self.host = host
        self.port = port
        os.makedirs(save_dir, exist_ok=True)
        self._server = None
        self.on_file_received = None

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"[+] Connected: {addr}")

        try:
            request = await read_message(reader)

            if request.get('type') == 'ping':
                response = create_message({"type": "pong"})
                writer.write(response)
                await writer.drain()
                return

            if request.get('type') != 'file_transfer_request':
                raise ValueError(f"Unknown type: {request.get('type')}")

            file_name = request['file_name']
            file_size = request['file_size']
            print(f"[*] Incoming: {file_name} ({file_size} bytes)")

            free_space = get_free_space(self.save_dir)
            if free_space < file_size:
                response = create_message({
                    "type": "file_transfer_response",
                    "accepted": False,
                    "message": f"No space. Free: {free_space // 1024 // 1024} MB"
                })
                writer.write(response)
                await writer.drain()
                return

            response = create_message({
                "type": "file_transfer_response",
                "accepted": True
            })
            writer.write(response)
            await writer.drain()

            filepath = os.path.join(self.save_dir, file_name)
            received = 0

            with open(filepath, 'wb') as f:
                while received < file_size:
                    remaining = file_size - received
                    chunk_size = min(CHUNK_SIZE, remaining)
                    chunk = await reader.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    received += len(chunk)

            if received == file_size:
                status = "ok"
                print(f"[✓] File saved: {file_name}")
                if self.on_file_received:
                    self.on_file_received(file_name)
            else:
                status = "error"
                print(f"[✗] Incomplete: {received}/{file_size}")
                try:
                    os.remove(filepath)
                except:
                    pass

            complete_msg = create_message({
                "type": "transfer_complete",
                "status": status,
                "bytes_received": received
            })
            writer.write(complete_msg)
            await writer.drain()
            await asyncio.sleep(0.3)

        except Exception as e:
            print(f"[!] Error: {e}")
            try:
                error_msg = create_message({
                    "type": "file_transfer_response",
                    "accepted": False,
                    "message": str(e)
                })
                writer.write(error_msg)
                await writer.drain()
            except:
                pass
        finally:
            writer.close()
            await writer.wait_closed()

    async def start(self):
        self._server = await asyncio.start_server(
            self.handle_client, self.host, self.port
        )
        print(f"[*] Server listening on {self.host}:{self.port}")

    async def stop(self):
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            print("[*] Server stopped")
