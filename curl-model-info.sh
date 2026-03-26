# curl-model-info.sh in https://github.com/bomonike/claude-templates/...
# Explaiined in https://bomonike.github.io/anthropic-certs/#Models
# BEFORE RUNNING:
# In Passowrd Manager: Copy into Clipboard the value of ANTHROPIC
# in Terminal: create command like this and invoke it:
#    export ANTHROPIC_API_KEY='sk-...'
#    chmod +x curl-model-info.sh
#    ./curl-model-info.sh

curl https://api.anthropic.com/v1/messages \
   -H "Content-Type: application/json" \
   -H "x-api-key: $ANTHROPIC_API_KEY" \
   -H "anthropic-version: 2023-06-01" \
   -d '{
      "model": "claude-haiku-4-5",
      "max_tokens": 1000,
      "messages": [
         {
         "role": "user",
         "content": "What are the capabilities of model claude-haiku-4-5 and its Reliable knowledge cutoff date and Training data cutoff dates?"
         }
      ]
   }'