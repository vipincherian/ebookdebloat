#!/bin/bash
#xterm -maximized -T Tmux -e "tmux new-session \\; split-window -v \\; resize-window -D 30 \\;attach "
#xterm -maximized -T Tmux -e "tmux new-session \\; split-window -v \\; resize-window -D 30 \\; attach "
if [[ ! -f ".iderc" ]]
then
  xmessage ".iderc file could not be found for sourcing."
  exit -1
fi

. .iderc

if [[ -z "$EDITOR_CMD" ]]
then
  xmessage "Variable EDITOR_CMD not set in .iderc."
  exit -1
fi

if [[ -z "$VENV_CMD" ]]
then
  xmessage "Variable VENV_CMD not set in .iderc."
  exit -1
fi

SESSION_NAME=project-ebookdebloat-session
#tmux new-session -d -s "$SESSION_NAME" "$EDITOR_CMD";
tmux new-session -d -s "$SESSION_NAME";
tmux send ". $VENV_CMD" ENTER;
tmux send "$EDITOR_CMD" ENTER;
tmux split-pane -v -p 10;

tmux resize-pane -y 4;
tmux send ". $VENV_CMD" ENTER;
tmux send 'cd src' ENTER; 

xterm -maximized -T "Project Ebook Debloat" -e "tmux attach -t $SESSION_NAME \\;"
tmux kill-session -t "$SESSION_NAME" 

