from transformers import Trainer, TrainingArguments, AutoModelForQuestionAnswering, AutoTokenizer
from datasets import load_dataset

dataset = load_dataset('json', data_files='perguntas_respostas_magic.json')

tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModelForQuestionAnswering.from_pretrained('bert-base-uncased')

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    save_steps=10_000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
)

trainer.train()

trainer.save_model('./results')
