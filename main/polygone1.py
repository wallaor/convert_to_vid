from create_frame import *
import time

# ANIM0003 не имеет фреймов 1 типа и парсится почти весь (206 из 207 фреймов)
# ANIM0006 парсит 205 из 204 фреймов (после парсинга первого фрейма - неизвестный блок), нет 04 типа фреймов
# ANIM0008 парсит 139 из 138 фреймов (после парсинга первого фрейма - неизвестный блок), нет 04 типа фреймов
# ANIM0012 парсит 125 из 130 фреймов (потерянных байтов не замечено), нет 01 типа фреймов
# ANIM0013 парсит 152 из 151 фрейма (потерянных байтов не замечено), есть оба типа сжатия, но так как все фреймы,
#      судя по всему, на месте, один фрейм - одно изменение картинки.
#      По ним можно попробовать понять НАСТОЯЩИЙ алгоритм сжатия обоих типов

#           Analys part
###########################################################################
example_file = open('../example/ANIM0013.VID', 'rb')
VID_file = example_file.read()
example_file.close()
total_founded_frames = 0
type_01 = False # наличие самого сложного метода сжатия
type_04 = False # наличие среднего по сложности метода сжатия

i = 0
while (i < len(VID_file)):
    if VID_file[i:i+3] == b'VID':
        print(f"this is header on {i} byte")
        count_of_frames = int.from_bytes(VID_file[i+5:i+7], byteorder = 'little')
        print("\tcount of frames = ", count_of_frames)
        resolution = [int.from_bytes(VID_file[i+7:i+9], byteorder = 'little'), int.from_bytes(VID_file[i+9:i+11], byteorder = 'little')]
        framebuffer = resolution[0] * resolution[1]
        print("\tresolution = ", resolution)
        global_delay = int.from_bytes(VID_file[i+11:i+13], byteorder = 'little')
        print("\tglobal delay = ", global_delay, ", time in second =", global_delay/60.0)
        print("\t",bytes(VID_file[i:i+15]))
        i=i+15
    if VID_file[i] == 2:
        print(f"this is palette on {i} byte")
        palette_bytes = bytes(VID_file[i+1:i + 769])
        print("\tin bytes: ", palette_bytes)
        i=i+769
        palette_colors = draw_frame('palette', 30, form_frame_by_hex_set(16, 16, palette_bytes))
    if VID_file[i] == 124:
        print(f"this is first audio frame on {i} byte")
        len_audio = int.from_bytes(VID_file[i+4:i+6], byteorder = 'little')
        i=i+6
        print("\tdata len =", len_audio, "bytes")
        print("\t", bytes(VID_file[i-6:i+len_audio ]))
        i=i+len_audio
    if VID_file[i] == 3:
        print(f"this is full frame of video type 03 on {i} byte")
        frame_show_time = int.from_bytes(VID_file[i+1:i+3], byteorder = 'little')
        i=i+3
        print("\tshow time =", frame_show_time, ", time in seconds =", frame_show_time/60.0)
        frame = []
        # realisation of RLE decompression
        while (len(frame) < framebuffer):
            current_byte = VID_file[i]
            if current_byte >= int.from_bytes(b'\x80', byteorder = 'little'):
                count_of_bytes = current_byte - int.from_bytes(b'\x80', byteorder = 'little')
                next_byte = VID_file[i+1]
                for x in range(count_of_bytes):
                    frame.append(next_byte)
                i = i + 2
            elif current_byte == 0:
                print("END OF FRAME?")
                time.sleep(1)
            else:
                count_of_non_repeat_bytes = current_byte
                next_bunch_of_bytes = VID_file[i+1:i+1+count_of_non_repeat_bytes]
                frame = frame + [byte for byte in next_bunch_of_bytes]
                i=i+1+count_of_non_repeat_bytes
        total_founded_frames+=1
        print(frame)
        draw_frame(total_founded_frames, 3, form_frame_by_palette(resolution[0], resolution[1], palette_colors, frame))
        time.sleep(5)
    if VID_file[i] == 125:
        print(f"this is regular audio frame on {i} byte")
        len_audio = int.from_bytes(VID_file[i + 1:i + 3], byteorder='little')
        i=i+3
        print("\tdata len =", len_audio, "bytes")
        print("\t", bytes(VID_file[i - 3:i + len_audio]))
        i = i + len_audio
    if VID_file[i] == 4:
        # define end of videoframe
        start_point = i
        while (start_point < len(VID_file)):
            if (VID_file[start_point] == 125) and (int.from_bytes(VID_file[start_point + 1:start_point + 3], byteorder='little') == len_audio):
                end_point = start_point-1
                break
            else:
                end_point = len(VID_file) - 1
            start_point=start_point+1
        # revert all changes with i
        print(f"this is compressed video frame type 04 started on {i} byte and ended on {end_point}")
        '''
        change_start_point =  int.from_bytes(VID_file[i+3:i+5], byteorder = 'little')
        i=i+5
        j = (change_start_point*resolution[0])-1
        while j<len(frame):
            current_byte = VID_file[i]
            if current_byte >= int.from_bytes(b'\x80', byteorder = 'little'):
                skip_bytes_count = current_byte - int.from_bytes(b'\x80', byteorder = 'little')
                i=i+1
                j=j+skip_bytes_count
                #print(f"skip {skip_bytes_count} bytes")
            elif current_byte < int.from_bytes(b'\x80', byteorder = 'little'):
                frame[j] = current_byte
                #print(f"rewrite {j+1} byte of frame on {current_byte}")
                i = i + 1
                j=j+1
                #time.sleep(2)
        print(frame)
                '''
        i = end_point
        total_founded_frames += 1
        type_04 = True
    if VID_file[i] == 1:
        # define end of videoframe
        start_point = i
        while (start_point < len(VID_file)):
            if (VID_file[start_point] == 125) and (
                    int.from_bytes(VID_file[start_point + 1:start_point + 3], byteorder='little') == len_audio):
                end_point = start_point - 1
                break
            else:
                end_point = len(VID_file) - 1
            start_point = start_point + 1
        # revert all changes with i
        print(f"this is compressed video frame type 01 started on {i} byte and ended on {end_point}")
        '''
        frame_show_time = int.from_bytes(VID_file[i + 1:i + 3], byteorder='little')
        i = i + 3
        print("\tshow time =", frame_show_time, ", time in seconds =", frame_show_time / 60.0)
        '''
        i = end_point
        total_founded_frames += 1
        type_01 = True

    if VID_file[i] == 20:
        print("the end")
        break

    print(i, VID_file[i])
    #time.sleep(3)
    i+=1

print(f"parsed frames: {total_founded_frames} of {count_of_frames}")
print(f"тип 04: {type_04}")
print(F"тип 01: {type_01}")

#           Create new file part
###########################################################################

# build info about new file
wideo_length = 5 # in seconds
resolution = [320, 200] # 320x200 pixels
global_delay_sec = 0.2 # base delay for each frame in seconds, looks like this is possible minimum

global_delay_for_frames = 1     # уточни!, предположительно 1 единица задержки = 1/5 секунды
count_of_frames = 500           # если одна единица задержки = 1/5 секунды, то 250 фреймов - 50 секунд видео
framebuffer_size = resolution[0] * resolution[1]

def create_picture_array_type03(color_number):
    header_of_type03_video = b'\x03\x00\x00'
    byte_color_number = color_number.to_bytes(1, 'little')
    count_of_repeat = framebuffer_size//127
    ostatok = framebuffer_size % 127
    repeated_part = (b'\xff' + byte_color_number) * count_of_repeat
    tail_part = ostatok.to_bytes(1, 'little')
    summ = header_of_type03_video + repeated_part + tail_part + byte_color_number
    return summ

def create_picture_array_type01(nodiff = True):
    if nodiff:
        pass

picture1s = create_picture_array_type03(0)
picture2s = create_picture_array_type03(0)

print(len(picture1s))

new_header = b'VID\x00\x02' + count_of_frames.to_bytes(2, 'little') + resolution[0].to_bytes(2, 'little') +\
             resolution[1].to_bytes(2, 'little') + global_delay_for_frames.to_bytes(2, 'little') + b'\x0e\x00'
new_palette = b'\x02' + palette
fake_audio_start = b'\x7c\x00\x00\xa6\x01\x79'
fake_middle_section = b'\x7d\x01\x79'

newfile = open('../out/out.vid', 'wb')
newfile.write(new_header)
newfile.write(new_palette)
#newfile.write(fake_audio_start)
newfile.write(picture2s)
#newfile.write((picture1s) * (count_of_frames//2))
#newfile.write((picture2s) * ((count_of_frames//2) + count_of_frames%2))
newfile.close()