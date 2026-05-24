(() => {
  const clamp = (value, low, high) => Math.max(low, Math.min(high, value));

  class DeckStage extends HTMLElement {
    connectedCallback() {
      this.width = Number(this.getAttribute('width')) || 1920;
      this.height = Number(this.getAttribute('height')) || 1080;
      this.index = 0;
      this.attachShadow({ mode: 'open' });
      this.shadowRoot.innerHTML = `
        <style>
          :host {
            position: fixed;
            inset: 0;
            display: block;
            overflow: hidden;
            background: #000000;
            font-family: 'Source Sans 3', 'Arial', sans-serif;
          }
          .stage {
            position: absolute;
            inset: 0;
            display: flex;
            align-items: center;
            justify-content: center;
          }
          .canvas {
            position: relative;
            width: ${this.width}px;
            height: ${this.height}px;
            transform-origin: center center;
            background: #ffffff;
          }
          ::slotted(*) {
            position: absolute !important;
            inset: 0 !important;
            width: 100% !important;
            height: 100% !important;
            visibility: hidden;
            opacity: 0;
            pointer-events: none;
          }
          ::slotted([data-deck-active]) {
            visibility: visible;
            opacity: 1;
            pointer-events: auto;
          }
          .hud {
            position: fixed;
            left: 50%;
            bottom: 24px;
            transform: translateX(-50%);
            padding: 8px 16px;
            border-radius: 999px;
            background: rgba(0, 0, 0, 0.72);
            color: #ffffff;
            font-size: 22px;
            line-height: 1.2;
            opacity: 0;
            transition: opacity 160ms ease;
            user-select: none;
          }
          .hud[data-visible] { opacity: 1; }
          @media print {
            :host {
              position: static;
              display: block;
              background: #ffffff;
              overflow: visible;
            }
            .stage, .canvas {
              position: static;
              display: block;
              transform: none !important;
              width: ${this.width}px;
              height: auto;
            }
            .hud { display: none; }
            ::slotted(*) {
              position: relative !important;
              visibility: visible;
              opacity: 1;
              page-break-after: always;
            }
          }
        </style>
        <div class="stage"><div class="canvas"><slot></slot></div></div>
        <div class="hud" aria-live="polite"></div>
      `;
      this.canvas = this.shadowRoot.querySelector('.canvas');
      this.hud = this.shadowRoot.querySelector('.hud');
      this.slides = Array.from(this.children).filter((el) => el.tagName.toLowerCase() === 'section');
      this.notes = this.readNotes();
      this.resize = this.resize.bind(this);
      this.onKey = this.onKey.bind(this);
      window.addEventListener('resize', this.resize);
      window.addEventListener('keydown', this.onKey);
      this.resize();
      this.go(0);
    }

    disconnectedCallback() {
      window.removeEventListener('resize', this.resize);
      window.removeEventListener('keydown', this.onKey);
    }

    readNotes() {
      const tag = document.getElementById('speaker-notes');
      if (!tag) return [];
      try {
        const payload = JSON.parse(tag.textContent || '{}');
        return Array.isArray(payload.notes) ? payload.notes : [];
      } catch {
        return [];
      }
    }

    resize() {
      const scale = Math.min(window.innerWidth / this.width, window.innerHeight / this.height);
      this.canvas.style.transform = `scale(${scale})`;
    }

    onKey(event) {
      if (event.key === 'ArrowRight' || event.key === 'PageDown' || event.key === ' ') {
        event.preventDefault();
        this.go(this.index + 1);
      } else if (event.key === 'ArrowLeft' || event.key === 'PageUp') {
        event.preventDefault();
        this.go(this.index - 1);
      } else if (event.key === 'Home') {
        event.preventDefault();
        this.go(0);
      } else if (event.key === 'End') {
        event.preventDefault();
        this.go(this.slides.length - 1);
      }
    }

    go(nextIndex) {
      if (!this.slides.length) return;
      this.index = clamp(nextIndex, 0, this.slides.length - 1);
      this.slides.forEach((slide, idx) => {
        if (idx === this.index) slide.setAttribute('data-deck-active', '');
        else slide.removeAttribute('data-deck-active');
      });
      const message = `${this.index + 1} / ${this.slides.length}`;
      this.hud.textContent = message;
      this.hud.setAttribute('data-visible', '');
      window.clearTimeout(this.hudTimer);
      this.hudTimer = window.setTimeout(() => this.hud.removeAttribute('data-visible'), 1200);
      window.postMessage({ slideIndexChanged: this.index, deckTotal: this.slides.length }, '*');
      this.dispatchEvent(new CustomEvent('slidechange', {
        bubbles: true,
        composed: true,
        detail: { index: this.index, total: this.slides.length, slide: this.slides[this.index], notes: this.notes[this.index] || '' }
      }));
    }
  }

  if (!customElements.get('deck-stage')) customElements.define('deck-stage', DeckStage);
})();
