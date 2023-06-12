import openai

openai.api_key = "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"

model_engine = "text-curie-001"
prompt = "Hello, how are you today?"

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Write a tagline for an ice cream shop."
)

print(response)



