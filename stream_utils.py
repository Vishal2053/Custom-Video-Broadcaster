import cv2
import pyvirtualcam
from engine import CustomerSegmenataionwithYolo
import torch


class Streaming(CustomerSegmenataionwithYolo):
    def __init__(self,in_source=None, fps= None, out_source=None, cam_fps = 15, blur_strength=None,background="none"):
        super().__init__(erode_size=5, erode_intensity=2)
        self.input_source = in_source
        self.out_source = out_source
        self.fps = fps
        self.blur_strength = blur_strength
        self.background = background
        self.original_fps = cam_fps
        self.running = False
        self.device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")

    def update_streamming_config(self,in_source=None, fps= None, out_source=None, blur_strength=None,background="none"):
        self.input_source = in_source
        self.out_source = out_source
        self.fps = fps
        self.blur_strength = blur_strength
        self.background = background
    
    def update_running_status(self, running_status=False):
        self.running = running_status



    def stream_video(self):
        self.running = True
        cap = cv2.VideoCapture(int(self.input_source))

        frame_idx = 0

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        try:
            self.original_fps = int(cap.get(cv2.CAP_PROP_FPS))
        except Exception as e:
            print(f"webcame {self.input_source} , live fps not available. Set the fps accordingly.")

        if self.fps:
            if self.fps > self.original_fps:
                print(f"Desired fps {self.fps} is greater than original fps {self.original_fps}. Setting fps to {self.original_fps}")
                self.fps = self.original_fps
                frame_interval = int(self.original_fps / self.fps)
            else:
                frame_interval = int(self.original_fps / self.fps)

        else:
            frame_interval = 1
        
        with pyvirtualcam.Camera(width=width, height=height, fps=self.fps,) as cam:
            print(f"Virtual camera running at: {width}x{height} at {self.fps} fps")

            while self.running and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_idx % frame_interval == 0:
                    results = self.model.predict(source = frame,save=False,save_txt=False,stream = True, retina_masks = True, verbose = False, device = self.device)
                    mask = self.generate_mask_from_result(results)
                    if mask is not None:
                        if self.background == "blur":
                            result_frame = self.apply_blur_with_mask(frame, mask, blur_strength=self.blur_strength)
                        elif self.background == "none":
                            result_frame = self.apply_black_background(frame, mask)
                        elif self.background == "default":
                            result_frame = self.apply_custom_background(frame, mask)
                    result_frame = 0
                frame_idx += 1
            cam.send(cv2.cvtColor(result_frame, cv2.COLOR_BGR2RGB))
            cam.sleep_until_next_frame()
        cap.release()


    def list_available_devices(self):
        devices = []
        index = 0
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.isOpened():
                break
            devices.append({"id": index, "name": f"Camera {index}"})
            cap.release()  # Always release the capture object
            index += 1
        return devices
