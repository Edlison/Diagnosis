# @Author  : Edlison
# @Date    : 8/6/21 02:29
from nlp.chatbot.run import load_pretrained, eval_sentence


def api_chatbot(msg):
    # Configure models
    attn_model = 'dot'
    hidden_size = 500
    encoder_n_layers = 2
    decoder_n_layers = 2
    dropout = 0.1

    # Set checkpoint to load from; set to None if starting from scratch
    # loadFilename = None
    loadFilename = 'nlp/chatbot/data/50000_checkpoint.tar'

    # run(loadFilename, model_name, corpus_name, batch_size, attn_model, hidden_size, encoder_n_layers, decoder_n_layers, dropout)
    searcher, voc = load_pretrained(loadFilename, attn_model, hidden_size, encoder_n_layers, decoder_n_layers, dropout)
    res = eval_sentence(msg, searcher, voc)

    return res