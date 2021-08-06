# @Author  : Edlison
# @Date    : 7/27/21 19:57
import torch
import torch.nn as nn
from nlp.chatbot.model import EncoderRNN, LuongAttnDecoderRNN
from nlp.chatbot.config import device
from nlp.chatbot.evaluation import GreedySearchDecoder, evaluate
from nlp.chatbot.preprocess import Voc, normalize_string


def load_pretrained(load_file, attn_model, hidden_size, encoder_n_layers, decoder_n_layers, dropout):
    voc = Voc('movie')
    # If loading on same machine the model was trained on
    checkpoint = torch.load(load_file, map_location=torch.device('cpu'))
    # If loading a model trained on GPU to CPU
    # checkpoint = torch.load(loadFilename, map_location=torch.device('cpu'))
    encoder_sd = checkpoint['en']
    decoder_sd = checkpoint['de']
    embedding_sd = checkpoint['embedding']
    voc.__dict__ = checkpoint['voc_dict']
    embedding = nn.Embedding(voc.num_words, hidden_size)
    embedding.load_state_dict(embedding_sd)
    # Initialize encoder & decoder models
    encoder = EncoderRNN(hidden_size, embedding, encoder_n_layers, dropout)
    decoder = LuongAttnDecoderRNN(attn_model, embedding, hidden_size, voc.num_words, decoder_n_layers, dropout)
    encoder.load_state_dict(encoder_sd)
    decoder.load_state_dict(decoder_sd)

    # Use appropriate device
    encoder = encoder.to(device)
    decoder = decoder.to(device)

    # Set dropout layers to eval mode
    encoder.eval()
    decoder.eval()

    # Initialize search module
    searcher = GreedySearchDecoder(encoder, decoder)

    return searcher, voc


def eval_sentence(msg, searcher, voc):
    try:
        # Normalize sentence
        input_sentence = normalize_string(msg)
        # Evaluate sentence
        output_words = evaluate(searcher, voc, input_sentence)
        # Format and print response sentence
        output_words[:] = [x for x in output_words if not (x == 'EOS' or x == 'PAD')]
        return ' '.join(output_words)
    except KeyError:
        return 'Try again.'


if __name__ == '__main__':
    # Configure models
    attn_model = 'dot'
    hidden_size = 500
    encoder_n_layers = 2
    decoder_n_layers = 2
    dropout = 0.1

    # Set checkpoint to load from; set to None if starting from scratch
    # loadFilename = None
    loadFilename = './data/50000_checkpoint.tar'

    # run(loadFilename, model_name, corpus_name, batch_size, attn_model, hidden_size, encoder_n_layers, decoder_n_layers, dropout)
    searcher, voc = load_pretrained(loadFilename, attn_model, hidden_size, encoder_n_layers, decoder_n_layers, dropout)
    res = eval_sentence('ooo', searcher, voc)
    print(res)

