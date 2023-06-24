#!/usr/bin/env python3
"""
NAME
    openai-transcribe - transcribes audio/video files using OpenAI's Whisper API

SYNOPSIS
    openai-transcribe [options] file...

DESCRIPTION
    openai-transcribe reads the specified audio and/or video files and
    transcribes them using OpenAI's Whisper API.

    The transcribed text is then printed to standard output.

OPTIONS
    --verbose
        Print progress before each major external step.

    file
        The audio or video file to transcribe. Multiple files can be
        specified.

EXAMPLES
    Transcribe a single video:
    openai-transcribe long-meeting.mp4 > long-meeting.txt

    Transcribe multiple files with verbose output:
    openai-transcribe --verbose chapter1.mp3 chapter2.mp3 chapter3.mp3 > book.txt

AUTHORS
    Written by GPT-4.
    Prompt engineering by Eric Hammond.

DATE
    2023-06-23
"""

import argparse
import os
import sys
import subprocess
from pydub import AudioSegment
import openai
import tempfile
import shutil
from moviepy.editor import VideoFileClip
import atexit

# Define constants
CHUNK_SIZE_IN_MIN = 10
CHUNK_SIZE_IN_MS = CHUNK_SIZE_IN_MIN * 60 * 1000
WHISPER_MODE = 'whisper-1'

def check_ffmpeg_installed():
    try:
        subprocess.check_output(['ffmpeg', '-version'])
    except FileNotFoundError:
        print("ffmpeg not found. Please install it before running this script.", file=sys.stderr)
        sys.exit(1)

def safe_remove(file_path):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass

def convert_video_to_audio(filename):
    try:
        handle, output_filename = tempfile.mkstemp(suffix=".mp3")
        os.close(handle)  # We don't need the open file handle
        atexit.register(safe_remove, output_filename)
        subprocess.run(['ffmpeg', '-i', filename, '-y', '-vn', '-acodec', 'libmp3lame', '-loglevel', 'error', output_filename])
    except Exception as e:
        print(f"Error while converting '{filename}' to audio: {e}", file=sys.stderr)
        return None
    return output_filename

def transcribe_audio(filename, verbose):
    try:
        audio = AudioSegment.from_mp3(filename)
    except Exception as e:
        print(f"Error while reading audio from '{filename}': {e}", file=sys.stderr)
        return None
    chunks = [audio[i:i + CHUNK_SIZE_IN_MS] for i in range(0, len(audio), CHUNK_SIZE_IN_MS)]

    transcripts = []
    for i, chunk in enumerate(chunks):
        if verbose:
            print(f"Converting audio to text: Chunk {i+1} out of {len(chunks)}", file=sys.stderr)
        handle, chunk_filename = tempfile.mkstemp(suffix=".mp3")
        os.close(handle)  # We don't need the open file handle
        atexit.register(safe_remove, chunk_filename)
        try:
            chunk.export(chunk_filename, format="mp3")
            with open(chunk_filename, "rb") as audio_file:
                transcript = openai.Audio.transcribe(WHISPER_MODE, audio_file)
                transcripts.append(transcript["text"])
        except Exception as e:
            print(f"Error while transcribing chunk {i} from '{filename}': {e}", file=sys.stderr)
        finally:
            safe_remove(chunk_filename)
    return transcripts

def is_video(file_path):
    try:
        clip = VideoFileClip(file_path)
        return True
    except Exception:
        return False

def handle_files(file_paths, verbose):  
    for i, file_path in enumerate(file_paths):
        if verbose:
            print(f"Processing file {i+1} out of {len(file_paths)}: {file_path}", file=sys.stderr)
        if len(file_paths) > 1:
            print(f"\n==> {file_path} <==")
        if is_video(file_path):
            if verbose:
                print("Converting video to audio", file=sys.stderr)
            audio_file = convert_video_to_audio(file_path)
            if audio_file is not None:
                if verbose:
                    print("Generating chunks of audio", file=sys.stderr)
                transcripts = transcribe_audio(audio_file, verbose)
                for transcript in transcripts:  # print the transcripts
                    print(transcript)
                safe_remove(audio_file)
        else:
            if verbose:
                print("Generating chunks of audio", file=sys.stderr)
            transcripts = transcribe_audio(file_path, verbose)
            for transcript in transcripts:  # print the transcripts
                print(transcript)

def parse_args():
    parser = argparse.ArgumentParser(description="Transcribe audio using OpenAI's Whisper API.")
    parser.add_argument('files', metavar='F', type=str, nargs='+', help='one or more files to transcribe')
    parser.add_argument('--verbose', action='store_true', help='print progress for each file')
    return parser.parse_args()

def main():
    check_ffmpeg_installed()
    args = parse_args()
    handle_files(args.files, args.verbose)

if __name__ == "__main__":
    main()
