from transformers import BertForQuestionAnswering, Trainer, TrainingArguments
from datasets import load_dataset

dataset = load_dataset("json", data_files="C:/Users/Lucas Dal Pra/Documents/GitHub/magicIA/NovaIA/perguntas_respostas_magic.json")

def preprocess_data(examples):
    examples['start_positions'] = [1] * len(examples['input_ids']) 
    examples['end_positions'] = [2] * len(examples['input_ids'])
    return examples

train_dataset = dataset['train'].map(preprocess_data)

model = BertForQuestionAnswering.from_pretrained('bert-base-uncased')

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_dir='./logs',
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

trainer.train()
