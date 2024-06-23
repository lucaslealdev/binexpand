import os
import argparse

def get_file_size(file_path):
    return os.path.getsize(file_path)

def create_dummy_file(file_path, size):
    with open(file_path, 'wb') as f:
        f.write(b'\x00' * size)

def append_files(original_file, dummy_file, output_file):
    with open(output_file, 'wb') as out_f:
        with open(original_file, 'rb') as orig_f:
            out_f.write(orig_f.read())
        with open(dummy_file, 'rb') as dummy_f:
            out_f.write(dummy_f.read())

def get_track_count(cue_file_path):
    with open(cue_file_path, 'r') as f:
        cue_content = f.readlines()

    track_count = sum(1 for line in cue_content if line.strip().startswith('TRACK'))
    return track_count

def get_bin_file_from_cue(cue_file_path):
    with open(cue_file_path, 'r') as f:
        for line in f:
            if line.strip().startswith('FILE'):
                bin_file = line.split('"')[1]
                # Join with cue file directory to get full path
                return os.path.join(os.path.dirname(cue_file_path), bin_file)
    raise ValueError("BIN file not found in CUE file")

def update_cue_file(cue_file_path, output_bin_file, original_bin_file_size, track_count):
    with open(cue_file_path, 'r') as f:
        cue_content = f.readlines()

    # Calculate the start time for the new dummy track in mm:ss:ff format
    sectors = original_bin_file_size // 2352
    minutes = sectors // (60 * 75)
    seconds = (sectors % (60 * 75)) // 75
    frames = sectors % 75
    start_time = f'{minutes:02}:{seconds:02}:{frames:02}'

    new_track_number = track_count + 1

    # Add the new track information to the CUE content
    cue_content.append(f'TRACK {new_track_number:02} MODE1/2352\n')
    cue_content.append(f'    INDEX 01 {start_time}\n')

    with open(cue_file_path, 'w') as f:
        f.writelines(cue_content)

def pad_bin_cue(cue_file, output_bin_file):
    bin_file = get_bin_file_from_cue(cue_file)
    
    sector_size = 2352
    total_sectors = 359843
    cd_size = total_sectors * sector_size

    original_size = get_file_size(bin_file)
    padding_size = cd_size - original_size

    if padding_size > 0:
        dummy_file = os.path.join(os.path.dirname(cue_file), 'dummy_track.bin')
        create_dummy_file(dummy_file, padding_size)
        append_files(bin_file, dummy_file, output_bin_file)

        track_count = get_track_count(cue_file)
        update_cue_file(cue_file, output_bin_file, original_size, track_count)

        os.remove(dummy_file)
        print(f'Successfully padded the BIN file to {output_bin_file} and updated the CUE file.')
    else:
        print('The BIN file is already larger than the target CD size.')

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f'Successfully deleted {file_path}')
    except FileNotFoundError:
        print(f'File {file_path} not found.')
    except Exception as e:
        print(f'Error occurred while deleting {file_path}: {e}')

def rename_file(source, destination):
    try:
        os.rename(source, destination)
        print(f'Successfully renamed {source} to {destination}')
    except FileNotFoundError:
        print(f'File {source} not found.')
    except Exception as e:
        print(f'Error occurred while renaming {source} to {destination}: {e}')

def main():
    parser = argparse.ArgumentParser(description="Pad a BIN file to fill an entire CD and update the CUE file accordingly.")
    parser.add_argument("cue_file", help="The path to the CUE file.")
    args = parser.parse_args()

    cue_file = os.path.abspath(args.cue_file)
    output_bin_file = os.path.join(os.path.dirname(cue_file), 'padded_image.bin')
    
    pad_bin_cue(cue_file, output_bin_file)
    
    bin_file = get_bin_file_from_cue(cue_file)
    delete_file(bin_file)
    rename_file(output_bin_file, bin_file)

if __name__ == "__main__":
    main()
