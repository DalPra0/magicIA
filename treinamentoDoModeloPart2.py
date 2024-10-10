from transformers import BertForQuestionAnswering, Trainer, TrainingArguments
from datasets import load_dataset

# Carregar seu dataset - ajuste o caminho conforme necessário
dataset = load_dataset("json", data_files="C:/Users/Lucas Dal Pra/Documents/GitHub/magicIA/NovaIA/perguntas_respostas_magic.json")

# Função de pré-processamento
def preprocess_data(examples):
    # Aqui você deve incluir a lógica para determinar os índices de início e fim das respostas
    examples['start_positions'] = [1] * len(examples['input_ids'])  # Substitua pela lógica real
    examples['end_positions'] = [2] * len(examples['input_ids'])    # Substitua pela lógica real
    return examples

# Aplicar o pré-processamento
train_dataset = dataset['train'].map(preprocess_data)

# Carregar o modelo
model = BertForQuestionAnswering.from_pretrained('bert-base-uncased')

# Configurar os argumentos de treinamento
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_dir='./logs',
)

# Inicializar o Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

# Iniciar o treinamento
trainer.train()
