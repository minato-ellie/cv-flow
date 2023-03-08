import pytest

from cvflow.io.input.video import *


def test_video_stream_reader(monkeypatch):
    reader = VideoStreamReader('demos/sample.mp4')
    assert reader.next()[1].shape == (2160, 3840, 3)  # (height, width, channel)
    reader.close()

    with VideoStreamReader('demos/sample.mp4') as reader:
        for index, frame in reader:
            assert frame.shape == (2160, 3840, 3)
            if index == 10:
                break


def test_video_stream_reader_close(monkeypatch):
    def close(self):
        raise RuntimeError('close')

    monkeypatch.setattr(VideoStreamReader, 'close', close)

    reader = VideoStreamReader('demos/sample.mp4')

    with pytest.raises(RuntimeError):
        reader.__del__()

    with pytest.raises(RuntimeError):
        with VideoStreamReader('demos/sample.mp4') as _:
            pass


def test_video_stream_reader_correct(tmp_path):
    """
    Test if the video stream reader can read the correct frame

    Write a test video which has
    pure red in the first frame,
    pure green in the second frame,
    and pure blue in the third frame.
    """
    frame_1 = np.zeros((4, 4, 3), dtype=np.uint8)
    frame_1[:, :, 0] = 100
    frame_2 = np.zeros((4, 4, 3), dtype=np.uint8)
    frame_2[:, :, 1] = 100
    frame_3 = np.zeros((4, 4, 3), dtype=np.uint8)
    frame_3[:, :, 2] = 100
    frames = [frame_1, frame_2, frame_3]

    writer = cv2.VideoWriter(str(tmp_path / 'test.avi'), cv2.VideoWriter_fourcc(*'I444'), 1, (4, 4))
    for frame in frames:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        writer.write(frame)
    writer.release()

    # Read the video and check the frame
    reader = VideoStreamReader(str(tmp_path / 'test.avi'))
    for index, frame in reader:
        assert np.all((frame > 0) == (frames[index - 1] > 0))  # index starts from 1
    reader.close()

    # Read the video and check the frame
    with VideoStreamReader(str(tmp_path / 'test.avi')) as reader:
        for index, frame in reader:
            assert np.all((frame > 0) == (frames[index - 1] > 0))  # index starts from 1


def test_video_url_reader():
    reader = VideoUrlReader('https://mazwai.com/videvo_files/video/free/2018-12/small_watermarked/180607_A_124_preview.mp4')
    frame = reader.next()[1]
    assert isinstance(frame, np.ndarray)

    reader.close()

    with VideoUrlReader('https://mazwai.com/videvo_files/video/free/2018-12/small_watermarked/180607_A_124_preview.mp4') as reader:
        for index, frame in reader:
            assert isinstance(frame, np.ndarray)
            if index == 10:
                break


def test_video_device_reader():
    reader = VideoDeviceReader(0)
    frame = reader.next()[1]
    assert isinstance(frame, np.ndarray)

    reader.close()

    with VideoDeviceReader(0) as reader:
        for index, frame in reader:
            assert isinstance(frame, np.ndarray)
            if index == 10:
                break


def test_video_file_reader():
    reader = VideoFileReader('demos/sample.mp4')
    frame = reader.next()[1]
    assert isinstance(frame, np.ndarray)

    reader.close()

    with VideoFileReader('demos/sample.mp4') as reader:
        for index, frame in reader:
            assert isinstance(frame, np.ndarray)
            if index == 10:
                break
