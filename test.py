message = "lzh is :) , is :("
words =message.split(' ')
emojis = {}
emojis[":)"]="😊"
emojis[":("]="😭"
emojis["lzh"]="🐶"
emojis["lqh"]="🐷"

output=""
for w in words:
    newword=emojis.get(w,"🐯")
    output+=newword+" "

print(output)
print("ggggg")