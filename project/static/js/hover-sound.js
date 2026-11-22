// الفونكسيون الموحدة لتشغيل الصوت العادية
function addSoundEffect(selector, eventType, soundAudio) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(element => {
        element.addEventListener(eventType, () => {
            soundAudio.currentTime = 0;
            soundAudio.play();
        });
    });
}

const hoverSound = new Audio('/static/sounds/enter-sound.mp3');
const leaveSound = new Audio('/static/sounds/leave-sound.mp3');
const clickSound = new Audio('/static/sounds/click-sound.mp3');
const ChatBtn = new Audio('/static/sounds/chat-btn.mp3');
const Shair = new Audio('/static/sounds/shaire.mp3');
const LogOut = new Audio('/static/sounds/LogOut.mp3');
const Zoom = new Audio('/static/sounds/zome2.mp3');

addSoundEffect('.food-card', 'mouseenter', hoverSound);
addSoundEffect('.food-card', 'mouseleave', leaveSound);
addSoundEffect('.related-card', 'mouseenter', hoverSound);
addSoundEffect('.related-card', 'mouseleave', leaveSound);
addSoundEffect('.add-to-cart-btn', 'click', clickSound);
addSoundEffect('.product-add-btn', 'click', clickSound);
addSoundEffect('.close-modal-btn', 'click', clickSound);
addSoundEffect('.chat-btn', 'click', ChatBtn);
addSoundEffect('.logout', 'click', LogOut);
addSoundEffect('.product-thumbnails', 'click', Zoom);


const submitBtn = document.querySelector('.submit-order-btn');
if (submitBtn) {
    submitBtn.addEventListener('click', (e) => {
        Shair.currentTime = 0;
        Shair.play();
    });
}