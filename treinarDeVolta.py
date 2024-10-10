from transformers import Trainer, TrainingArguments, AutoModelForQuestionAnswering, AutoTokenizer
from datasets import load_dataset

# Carregar o dataset de perguntas e respostas
dataset = load_dataset('json', data_files='perguntas_respostas_magic.json')

# Carregar o modelo e tokenizer
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModelForQuestionAnswering.from_pretrained('bert-base-uncased')

# Definir argumentos para o treinamento
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    save_steps=10_000,
    save_total_limit=2,
)

# Treinador
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
)

# Treinar o modelo
trainer.train()

# Salvar o modelo
trainer.save_model('./results')
