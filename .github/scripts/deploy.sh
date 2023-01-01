# Setup ssh
mkdir -p "$HOME"/.ssh
ssh-keyscan "$SERVER_ADDRESS" >> "$HOME"/.ssh/known_hosts
eval "$(ssh-agent)"
ssh-add - <<< "$SSH_PRIVATE_KEY"

# Update docker-compose
envsubst < prod/docker-compose.template.yml > prod/docker-compose.yml
scp prod/docker-compose.yml "$SSH_USERNAME@$SERVER_ADDRESS:/data/sakuva/docker-compose.yml"

# Pull and restart changed
ssh "$SSH_USERNAME@$SERVER_ADDRESS" "
  cd /data/sakuva
  sudo docker-compose pull --quiet
  sudo docker-compose up -d
"
