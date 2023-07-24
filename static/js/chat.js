
var quill = new Quill('.editor', {
    modules: {
        toolbar: [
            [{ size: ['small', false, 'large', 'huge'] }],
            ['bold', 'italic', 'underline'],
            ['image', 'link']
        ]
    },
    theme: 'snow',
    placeholder: '阿巴阿巴（°∀。）...'
});

font_sizes = {
    "normal": "1.0em",
    "small": "0.75em",
    "large": "1.5em",
    "huge": "2.5em"
}

class Message {
    constructor() {
        this.messageContainer = document.createElement('div');
        this.messageContainer.classList.add('mdui-row', 'message-content');
        this.headerContainer = document.createElement('div');
        this.headerContainer.classList.add('mdui-row', 'message-header');
    }

    static col(element, ...column) {
        var div = document.createElement('div');
        div.classList.add(...column.map(x => 'mdui-col-' + x));
        div.appendChild(element);
        return div;
    }

    #appendBase() {
        var tag = document.createElement('div');
        tag.classList.add('message');
        return tag;
    }

    setSender(sender) {
        if (sender.avatar) {
            var avatar = document.createElement('img');
            avatar.classList.add('message-avatar', 'mdui-center');
            avatar.src = '/media/' + sender.avatar;
            this.headerContainer.appendChild(Message.col(avatar, 'md-1', 'xs-2'));
        }
        var col = document.createElement('div');
        col.classList.add('mdui-col-md-11', 'mdui-col-xs-10', 'mdui-valign');
        if (sender.nickname) {
            var nickname = document.createElement('span');
            nickname.innerText = sender.nickname;
            nickname.classList.add('message-username');
            col.appendChild(nickname);
        }
        if (sender.title) {
            var title = document.createElement('span');
            title.classList.add('user-title', 'user-title-level-' + sender.title_level);
            title.innerText = sender.title;
            col.appendChild(title);
        }
        this.headerContainer.appendChild(col);
    }

    appendText(text, attr) {
        var base = this.#appendBase();
        var tag = document.createElement('span');
        tag.innerText = text;
        if (attr) {
            if (attr.bold) {
                var _ = document.createElement('b');
                _.appendChild(tag);
                tag = _;
            }
            if (attr.underline) {
                var _ = document.createElement('u');
                _.appendChild(tag);
                tag = _;
            }
            if (attr.italic) {
                var _ = document.createElement('i');
                _.appendChild(tag);
                tag = _;
            }
            if (attr.link) {
                var _ = document.createElement('a');
                _.setAttribute('href', attr.link)
                _.appendChild(tag);
                tag = _;
            }
            if (attr.size) {
                tag.style.fontSize = font_sizes[attr.size];
            }
        }
        base.appendChild(tag);
        this.messageContainer.appendChild(Message.col(base, 'offset-xs-1'));
    }

    appendNotice(text) {
        // var base = this.#appendBase();
        // var icon = document.createElement('i');
        // icon.classList.add('mdui-icon', 'material-icons');
        // icon.innerText = 'notifications_active';
        // base.appendChild(icon);
        // base.appendChild(document.createTextNode(text));
        // this.messageContainer.appendChild(base);
    }

    appendImage(src) {
        var base = this.#appendBase();
        var img = document.createElement('img');
        img.setAttribute('src', src);
        base.appendChild(img);
        this.messageContainer.appendChild(Message.col(base, 'offset-xs-1'));
    }

    get empty() {
        return this.messageContainer.children.length == 0;
    }

    get container() {
        if (this.messageContainer.children.length == 0) {
            return null;
        }
        var container = document.createElement('div');
        container.classList.add('mdui-container', 'message');
        container.appendChild(this.headerContainer);
        container.appendChild(this.messageContainer);
        return container;
    }
}

class MessageContainer {
    constructor(container) {
        this.container = container;
    }
    append(msg) {
        if (!msg.empty) {
            this.container.appendChild(msg.container);
        }
    }
}

container = new MessageContainer(document.querySelector('.message-container'));

if (location.port) {
    path = `${location.hostname}:${location.port}/room/1/`;
}
else {
    path = `${location.hostname}/room/1/`;
}

socket = new WebSocket(`ws://${path}`);
sender = {
    username: document.getElementById('input-username').value,
    nickname: document.getElementById('input-nickname').value,
    avatar: document.getElementById('input-useravatar').value,
    title: document.getElementById('input-usertitle').value,
    title_level: document.getElementById('input-usertitle_level').value
};

socket.onmessage = function (event) {
    data = JSON.parse(event.data);

    msg = new Message();

    if (data.sender) {
        msg.setSender(data.sender);
    }

    data.message.forEach(i => {
        if (i.type == 'text') {
            msg.appendText(i.data, i.attr)
        }
        else if (i.type == 'notice') {
            msg.appendNotice(i.data);
        }
        else if (i.type == 'image') {
            msg.appendImage(i.data);
        }
    });

    container.append(msg);
}

document.querySelector('.editor').addEventListener('keydown', (e) => {
    if (e.key == 'Enter' && e.ctrlKey) {
        document.getElementById('send-button').click();
    }
});

socket.onopen = function (event) {
    socket.send(JSON.stringify({
        "init": true,
        "sender": sender,
        "message": []
    }));
}

function send() {
    let delta = quill.getContents();
    msg = [];
    if (delta.ops.length == 1 && delta.ops[0].insert.trim().length == 0) {
        mdui.snackbar('消息不能为空');
        return;
    }
    delta.ops.forEach(x => {
        if (x.insert.image) {
            msg.push({
                'type': 'image',
                'data': x.insert.image
            });
        }
        else if (typeof x.insert == 'string') {
            msg.push({
                'type': 'text',
                'data': x.insert,
                'attr': x.attributes
            });
        }
    });
    socket.send(JSON.stringify({
        "sender": sender,
        "message": msg
    }));
    quill.deleteText(0, quill.getLength());
}
