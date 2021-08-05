# @Author  : Edlison
# @Date    : 7/25/21 11:19
import csv
import itertools
import os
import random
import re
import codecs
import unicodedata
from config import SOS_token, EOS_token, PAD_token, MAX_LENGTH


# Format
import torch


def read_lines(file_name, n=10):
    with open(file_name, 'rb') as f:
        lines = f.readlines()
    for i in lines[:n]:
        print(i)


def _load_lines(file_name, fields):
    lines = {}
    with open(file_name, 'r', encoding='iso-8859-1') as f:
        for line in f:
            values = line.split(' +++$+++ ')
            line = {}
            for i, field in enumerate(fields):
                line[field] = values[i]
            lines[line['lineID']] = line
    return lines


def _load_conversations(file_name, lines, fields):
    conversations = []
    with open(file_name, 'r', encoding='iso-8859-1') as f:
        for line in f:
            values = line.split(' +++$+++ ')
            conve = {}
            for i, field in enumerate(fields):
                conve[field] = values[i]
            utterance_id_pattern = re.compile('L[0-9]+')
            line_ids = utterance_id_pattern.findall(conve['utteranceIDs'])
            conve['lines'] = []
            for line_id in line_ids:
                conve['lines'].append(lines[line_id])  # append text from lines by line_id
            conversations.append(conve)
    return conversations


def _extract_sentence_pairs(conversations):
    qa_pairs = []
    for conversation in conversations:
        # Iterate over all the lines of the conversation
        for i in range(len(conversation["lines"]) - 1):  # We ignore the last line (no answer for it)
            input_line = conversation["lines"][i]["text"].strip()
            target_line = conversation["lines"][i+1]["text"].strip()
            # Filter wrong samples (if one of the lists is empty)
            if input_line and target_line:
                qa_pairs.append([input_line, target_line])
    return qa_pairs


def format_data():
    file_lines = './data/movie_lines.txt'
    file_conversations = './data/movie_conversations.txt'
    MOVIE_LINES_FIELDS = ["lineID", "characterID", "movieID", "character", "text"]
    MOVIE_CONVERSATIONS_FIELDS = ["character1ID", "character2ID", "movieID", "utteranceIDs"]
    lines = _load_lines(file_lines, MOVIE_LINES_FIELDS)
    conversations = _load_conversations(file_conversations, lines, MOVIE_CONVERSATIONS_FIELDS)
    pairs = _extract_sentence_pairs(conversations)
    file_formatted = './data/formatted.txt'
    delimiter = '\t'
    delimiter = str(codecs.decode(delimiter, 'unicode_escape'))
    with open(file_formatted, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=delimiter, lineterminator='\n')
        for pair in pairs:
            writer.writerow(pair)
    read_lines(file_formatted)


# Trim data
# Default word tokens



class Voc:
    def __init__(self, name):
        self.name = name
        self.trimmed = False
        self.word2index = {}
        self.word2count = {}
        self.index2word = {PAD_token: "PAD", SOS_token: "SOS", EOS_token: "EOS"}
        self.num_words = 3  # Count SOS, EOS, PAD

    def add_sentence(self, sentence):
        for word in sentence.split(' '):
            self.add_word(word)

    def add_word(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_words
            self.word2count[word] = 1
            self.index2word[self.num_words] = word
            self.num_words += 1
        else:
            self.word2count[word] += 1

    # Remove words below a certain count threshold
    def trim(self, min_count):
        if self.trimmed:
            return
        self.trimmed = True

        keep_words = []

        for k, v in self.word2count.items():
            if v >= min_count:
                keep_words.append(k)

        print('keep_words {} / {} = {:.4f}'.format(
            len(keep_words), len(self.word2index), len(keep_words) / len(self.word2index)
        ))

        # Reinitialize dictionaries
        self.word2index = {}
        self.word2count = {}
        self.index2word = {PAD_token: "PAD", SOS_token: "SOS", EOS_token: "EOS"}
        self.num_words = 3 # Count default tokens

        for word in keep_words:
            self.add_word(word)




def unicode_to_ascii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


# Lowercase, trim, and remove non-letter characters
def normalize_string(s):
    s = unicode_to_ascii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    s = re.sub(r"\s+", r" ", s).strip()
    return s


# Read query/response pairs and return a voc object
def read_vocs(datafile, corpus_name):
    print("Reading lines...")
    # Read the file and split into lines
    lines = open(datafile, encoding='utf-8').read().strip().split('\n')
    # Split every line into pairs and normalize
    pairs = [[normalize_string(s) for s in l.split('\t')] for l in lines]
    voc = Voc(corpus_name)
    return voc, pairs


# Returns True if both sentences in a pair 'p' are under the MAX_LENGTH threshold
def filter_pair(p):
    # Input sequences need to preserve the last word for EOS token
    return len(p[0].split(' ')) < MAX_LENGTH and len(p[1].split(' ')) < MAX_LENGTH


# Filter pairs using filterPair condition
def filter_pairs(pairs):
    return [pair for pair in pairs if filter_pair(pair)]


# Using the functions defined above, return a populated voc object and pairs list
def load_prepare_data(file_formatted, name):
    print("Start preparing training data ...")
    voc, pairs = read_vocs(file_formatted, name)
    print("Read {!s} sentence pairs".format(len(pairs)))
    pairs = filter_pairs(pairs)
    print("Trimmed to {!s} sentence pairs".format(len(pairs)))
    print("Counting words...")
    for pair in pairs:
        voc.add_sentence(pair[0])
        voc.add_sentence(pair[1])
    print("Counted words:", voc.num_words)
    return voc, pairs


def trim_rare_words(voc, pairs, MIN_COUNT):
    # Trim words used under the MIN_COUNT from the voc
    voc.trim(MIN_COUNT)
    # Filter out pairs with trimmed words
    keep_pairs = []
    for pair in pairs:
        input_sentence = pair[0]
        output_sentence = pair[1]
        keep_input = True
        keep_output = True
        # Check input sentence
        for word in input_sentence.split(' '):
            if word not in voc.word2index:
                keep_input = False
                break
        # Check output sentence
        for word in output_sentence.split(' '):
            if word not in voc.word2index:
                keep_output = False
                break

        # Only keep pairs that do not contain trimmed word(s) in their input or output sentence
        if keep_input and keep_output:
            keep_pairs.append(pair)

    print("Trimmed from {} pairs to {}, {:.4f} of total".format(len(pairs), len(keep_pairs), len(keep_pairs) / len(pairs)))
    return keep_pairs





# Prepare for model
def indexes_from_sentence(voc, sentence):
    return [voc.word2index[word] for word in sentence.split(' ')] + [EOS_token]


def zero_padding(l, fillvalue=PAD_token):
    return list(itertools.zip_longest(*l, fillvalue=fillvalue))


def binary_matrix(l, value=PAD_token):
    m = []
    for i, seq in enumerate(l):
        m.append([])
        for token in seq:
            if token == PAD_token:
                m[i].append(0)
            else:
                m[i].append(1)
    return m


# Returns padded input sequence tensor and lengths
def input_var(l, voc):
    indexes_batch = [indexes_from_sentence(voc, sentence) for sentence in l]
    lengths = torch.tensor([len(indexes) for indexes in indexes_batch])
    padList = zero_padding(indexes_batch)
    padVar = torch.LongTensor(padList)
    return padVar, lengths


# Returns padded target sequence tensor, padding mask, and max target length
def output_var(l, voc):
    indexes_batch = [indexes_from_sentence(voc, sentence) for sentence in l]
    max_target_len = max([len(indexes) for indexes in indexes_batch])
    padList = zero_padding(indexes_batch)
    mask = binary_matrix(padList)
    mask = torch.BoolTensor(mask)
    padVar = torch.LongTensor(padList)
    return padVar, mask, max_target_len


# Returns all items for a given batch of pairs
def batch_to_train_data(voc, pair_batch):
    pair_batch.sort(key=lambda x: len(x[0].split(" ")), reverse=True)
    input_batch, output_batch = [], []
    for pair in pair_batch:
        input_batch.append(pair[0])
        output_batch.append(pair[1])
    inp, lengths = input_var(input_batch, voc)
    output, mask, max_target_len = output_var(output_batch, voc)
    return inp, lengths, output, mask, max_target_len





if __name__ == '__main__':
    ...