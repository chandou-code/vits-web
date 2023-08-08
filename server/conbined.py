import ffmpeg
import os


class ffmpeg_:
    def ffmpeg__(self, content_list):
        import ffmpeg
        import os

        inputs = []
        for file in content_list:
            inputs.append(ffmpeg.input(file))

        filename = 'final.wav'
        output = ffmpeg.concat(*inputs, v=0, a=1).output(filename, y='-y')

        ffmpeg.run(output)

        for file_name in content_list:
            if os.path.exists(file_name):
                os.remove(file_name)
                # print(f"已删除临时文件: {file_name}")
            # else:
                # print(f"临时文件不存在: {file_name}")

        return filename
