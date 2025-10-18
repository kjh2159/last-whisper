import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Audio/Video Transcription Tool')
    
    # Manual input setting (can set only one between URL and local file)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-u', '--url', 
                             nargs='+',
                             help='YouTube or other video URL to transcribe')
    input_group.add_argument('-f', '--file',
                             nargs='+',
                             help='Local audio/video file path to transcribe')
    
    # extra options
    parser.add_argument('-m', '--model',
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       default='base',
                       help='Whisper model size (default: base)')
    parser.add_argument('-l', '--language',
                       default=None,
                       help='Language spoken in audio [en, ko, Japanese, ...]')
    parser.add_argument('-v', '--verbose',
                       action='store_true',
                       help='Show detailed transcription progress')
    parser.add_argument('-t', '--timeline',
                       action='store_true',
                       help='Show detailed transcription progress')
    
    return parser.parse_args()