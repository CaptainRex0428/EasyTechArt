from openai import OpenAI

client = OpenAI(
  api_key=""
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": r"为什么我不能通过API接入GPT-4o呢 只能接入4o-mini？"}
  ]
)

print(completion.choices[0].message);
