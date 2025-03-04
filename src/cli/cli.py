from datetime import date, datetime

from src.adapter import Adapter
from src.app import App
from src.cli.save import Save
from src.constants import VALID_EXTS
from src.logger import Logger

DEFAULT_DIR = f"./dump/{date.today()}"
DEFAULT_FNAME = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}"


class CLI:
    f"""
    valid file extensions: {VALID_EXTS}
    """
    logger: Logger

    def __init__(self: "CLI") -> None:
        self.logger = Logger()
        self.logger.log(
            """
               ____                          ____                 
              / ____ _____ ___ ___________  / / ___ ____ ____ ____
             _\ \/ // / _ / -_/ __/ __/ _ \/ / / _ `/ _ `/ -_/ __/
            /___/\_,_/ .__\__/_/  \__/\___/_/_/\_,_/\_, /\__/_/   
                    /_/                            /___/          
            """  # noqa
        )
        return

    def collage(
        self: "CLI",
        *inputs: str,
        fname: str = DEFAULT_FNAME,
        dir: str = DEFAULT_DIR,
        **kwargs,
    ) -> None:
        """
        Make a collage:
        ---
        Inputs:
            an image or images via url(s), filepath(s) or directory(s)
        Flags:
            -background: int|tuple, for background colour
            -color: float, post-process colour amount
            -contrast: float, post-process contrast amount
            -dir: str, directory to save to
            -fname: str, file name to save as
            -rotate: bool|float, either True (90°) or angle in deg
            -shuffle: bool, whether to shuffle input images
        """
        save = Save(fname=fname, dir=dir)
        imgs = Adapter.load(*inputs)
        self.logger.log("collaging images:")
        collages = App.collage(imgs, **kwargs)
        save.jpg(*collages)
        self.logger.log(f"saved to {dir}/{fname}-{0}.jpg")
        return

    def segment(
        self: "CLI",
        *inputs: str,
        fname: str = DEFAULT_FNAME,
        dir: str = DEFAULT_DIR,
        **kwargs,
    ) -> None:
        """
        Cuts out segments:
        ---
        Inputs:
            an image or images via url(s), filepath(s) or directory(s)
        Flags:
            -dir: str, directory to save to
            -fname: str, file name to save as
            -rotate: bool|float, either True (90°) or angle in deg
            -shuffe: bool, whether to shuffle input images
        """
        save = Save(fname=fname, dir=dir)
        imgs = Adapter.load(*inputs)
        self.logger.log("segmenting images:")
        segments = App.segment(imgs, **kwargs)
        save.png(*segments)
        self.logger.log(f"saved to {dir}")
        return

    def masks(
        self: "CLI",
        *inputs: str,
        fname: str = DEFAULT_FNAME,
        dir: str = DEFAULT_DIR,
        **kwargs,
    ) -> None:
        """
        Generates alpha masks of segments:
        ---
        Inputs:
            an image or images via url(s), filepath(s) or directory(s)
        Flags:
            -dir: str, directory to save to
            -fname: str, file name to save as
        """
        save = Save(fname=fname, dir=dir)
        imgs = Adapter.load(*inputs)
        self.logger.log("segmenting images:")
        masks = App.masks(imgs, **kwargs)
        save.png(*masks)
        self.logger.log(f"saved to {dir}")
        return

    def alpha_matte(
        self: "CLI",
        *inputs: str,
        fname: str = DEFAULT_FNAME,
        dir: str = DEFAULT_DIR,
        **kwargs,
    ) -> None:
        """
        Produces an alpha matte for objects in video
        ---
        Inputs:
            a video file
        Flags:
            -blur: float, blur mask
            -confidence_threshold: float, confidence for segment mask inclusion
            -dir: str, directory to save to
            -fname: str, file name to save as
            -gain: float, boost mask
            -keyframe_interval: int, how often to use a keyframe
        """
        save = Save(fname=fname, dir=dir)
        videos = Adapter.video(*inputs)
        self.logger.log("segmenting videos:")
        for video in videos:
            alpha = App.alpha_matte(video, **kwargs)
            save.mp4(alpha, fps=video.fps)
            video.close()
        return

    def super_resolution(
        self: "CLI",
        *inputs: str,
        fname: str = DEFAULT_FNAME,
        dir: str = DEFAULT_DIR,
        **kwargs,
    ) -> None:
        """
        Produces an alpha matte for objects in video
        ---
        Inputs:
            an image or images via url(s), filepath(s) or directory(s)
        Flags:
            -device: str, torch device for GPU ("cuda") or CPU ("cpu")
            -dir: str, directory to save to
            -dsize: tuple[int, int], target size of output image (w, h)
            -fname: str, file name to save as
        """
        save = Save(fname=fname, dir=dir)
        imgs = Adapter.load(*inputs)
        self.logger.log("upscaling images")
        supers = App.super_resolution(imgs, **kwargs)
        save.jpg(*supers)
        self.logger.log(f"saved to {dir}")
        return

    def abstract(
        self: "CLI",
        *inputs: str,
        fname: str = DEFAULT_FNAME,
        dir: str = DEFAULT_DIR,
        **kwargs,
    ) -> None:
        """
        Produces an abstract composition
        ---
        Inputs:
            an image or images via url(s), filepath(s) or directory(s)
        Flags:
            -color: float, post-process colour amount
            -contrast: float, post-process contrast amount
            -dir: str, directory to save to
            -dsize: tuple[int, int], target size of output image (w, h)
            -fname: str, file name to save as
            -limit: int, how many segments to cut from input images
            -n_segments: int, how many segments to use in composition
            -rotate: bool, whether to rotate alpha masks (default False)
        """
        save = Save(fname=fname, dir=dir)
        imgs = Adapter.load(*inputs)
        self.logger.log("making abstract composition")
        abstracts = App.abstracts(imgs, **kwargs)
        save.jpg(*abstracts)
        self.logger.log(f"saved to {dir}/{fname}-{0}.jpg")
        return


if __name__ == "__main__":
    from fire import Fire  # type: ignore

    Fire(CLI())
