
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

function append_text(elem, data, attr) {
    tag = document.createElement('span');
    tag.innerText = data;
    if (attr) {
        if (attr.bold) {
            _ = document.createElement('b');
            _.appendChild(tag);
            tag = _;
        }
        if (attr.underline) {
            _ = document.createElement('u');
            _.appendChild(tag);
            tag = _;
        }
        if (attr.italic) {
            _ = document.createElement('i');
            _.appendChild(tag);
            tag = _;
        }
        if (attr.link) {
            _ = document.createElement('a');
            _.setAttribute('href', attr.link)
            _.appendChild(tag);
            tag = _;
        }
        if (attr.size) {
            tag.style.fontSize = font_sizes[attr.size];
        }
    }
    elem.appendChild(tag);
}

function append_notice(elem, text) {
    icon = document.createElement('i');
    icon.classList.add('mdui-icon', 'material-icons');
    icon.innerText = 'notifications_active';
    elem.appendChild(icon);
    elem.appendChild(document.createTextNode(text));
}

function append_image(elem, src) {
    img = document.createElement('img');
    img.setAttribute('src', src);
    console.log(src);
    elem.appendChild(img);
}

socket = new WebSocket(`ws://${location.hostname}:8000/room/1/`);
username = document.getElementById('input-username').value;
nickname = document.getElementById('input-nickname').value;

socket.onmessage = function (event) {
    msg = document.createElement("div");
    data = JSON.parse(event.data);
    if (data.sender) {
        msg.appendChild(document.createTextNode(data.sender + ': '));
    }
    data.message.forEach(i => {
        if (i.type == 'text') {
            append_text(msg, i.data, i.attr)
        }
        else if (i.type == 'notice') {
            append_notice(msg, i.data);
        }
        else if (i.type == 'image') {
            append_image(msg, i.data);
        }
    });
    document.getElementById("message").appendChild(msg);
}

socket.onopen = function (event) {
    socket.send(JSON.stringify({
        "init": true,
        "sender": nickname,
        "message": []
    }));
    let tag = document.createElement("div");
    append_notice(tag, 'Connected');
    document.getElementById("message").appendChild(tag);
}

function send() {
    let delta = quill.getContents();
    msg = []
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
        "sender": nickname,
        "message": msg
    }));
}
