let Embed = Quill.import('blots/embed');
let Delta = Quill.import('delta');

class Mention extends Embed {
    static create(value) {
        let node = super.create();
        node.classList.add('mention');
        node.setAttribute('mention', value);
        node.innerText = '@' + value;
        return node;
    }

    static value(node) {
        return node.attributes.mention.value;
    }
}
Mention.blotName = 'mention';
Mention.tagName = 'span';

Quill.register(Mention);
