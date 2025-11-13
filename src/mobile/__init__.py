from src.mobile.views import MobileState
from src.tree import Tree
import uiautomator2 as u2
from io import BytesIO
from PIL import Image

class Mobile:
    def __init__(self,device:str=None):
        try:
            self.device = u2.connect(device)
            self.device.info
        except u2.ConnectError as e:
            raise ConnectionError(f"Failed to connect to device {device}: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error connecting to device {device}: {e}")

    def get_device(self):
        return self.device

    def get_state(self,use_vision=False, max_elements=50):
        import sys
        try:
            print(f"[Mobile.get_state] Creating Tree object...", file=sys.stderr, flush=True)
            tree = Tree(self)
            print(f"[Mobile.get_state] Getting tree state with max_elements={max_elements}...", file=sys.stderr, flush=True)
            tree_state = tree.get_state(max_elements=max_elements)
            print(f"[Mobile.get_state] Tree state obtained, {len(tree_state.interactive_elements)} elements", file=sys.stderr, flush=True)
            if use_vision:
                print(f"[Mobile.get_state] Generating screenshot...", file=sys.stderr, flush=True)
                nodes=tree_state.interactive_elements
                # Use smaller scale (0.4) to reduce image size and avoid input length limit
                annotated_screenshot=tree.annotated_screenshot(nodes=nodes,scale=0.4)
                screenshot=self.screenshot_in_bytes(annotated_screenshot, compress=True)
            else:
                screenshot=None
            print(f"[Mobile.get_state] Returning MobileState", file=sys.stderr, flush=True)
            return MobileState(tree_state=tree_state,screenshot=screenshot)
        except Exception as e:
            print(f"[Mobile.get_state] Error: {str(e)}", file=sys.stderr, flush=True)
            raise RuntimeError(f"Failed to get device state: {e}")
    
    def get_screenshot(self,scale:float=0.7)->Image.Image:
        try:
            screenshot=self.device.screenshot()
            if screenshot is None:
                raise ValueError("Screenshot capture returned None.")
            size=(screenshot.width*scale, screenshot.height*scale)
            screenshot.thumbnail(size=size, resample=Image.Resampling.LANCZOS)
            return screenshot
        except Exception as e:
            raise RuntimeError(f"Failed to get screenshot: {e}")
    
    def screenshot_in_bytes(self,screenshot:Image.Image, compress:bool=False)->bytes:
        try:
            if screenshot is None:
                raise ValueError("Screenshot is None")
            io=BytesIO()
            if compress:
                # Further compress to reduce size, aiming for <500KB
                quality = 60
                screenshot.save(io, format='JPEG', quality=quality, optimize=True)
                size_kb = len(io.getvalue()) / 1024
                # If still too large, reduce quality further
                while size_kb > 500 and quality > 20:
                    io = BytesIO()
                    quality -= 10
                    screenshot.save(io, format='JPEG', quality=quality, optimize=True)
                    size_kb = len(io.getvalue()) / 1024
            else:
                screenshot.save(io, format='PNG', optimize=True)
            bytes=io.getvalue()
            if len(bytes) == 0:
                raise ValueError("Screenshot conversion resulted in empty bytes.")
            import sys
            print(f"[Mobile.screenshot_in_bytes] Screenshot size: {len(bytes)/1024:.1f}KB", file=sys.stderr, flush=True)
            return bytes
        except Exception as e:
            raise RuntimeError(f"Failed to convert screenshot to bytes: {e}")

    