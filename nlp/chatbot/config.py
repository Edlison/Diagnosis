# @Author  : Edlison
# @Date    : 7/27/21 20:00
import torch


PAD_token = 0  # Used for padding short sentences
SOS_token = 1  # Start-of-sentence token
EOS_token = 2  # End-of-sentence token
MAX_LENGTH = 10  # Maximum sentence length to consider
MIN_COUNT = 3    # Minimum word count threshold for trimming



USE_CUDA = torch.cuda.is_available()
device = torch.device("cuda" if USE_CUDA else "cpu")