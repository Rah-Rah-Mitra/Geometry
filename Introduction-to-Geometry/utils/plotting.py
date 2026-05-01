from __future__ import annotations
PALETTE={"ink":"#1f2933","blue":"#2364aa","orange":"#f97316","green":"#2f9e44","red":"#d64545","gold":"#d4a017","violet":"#6f42c1","grid":"#d8dee9"}
def svg_escape(text: str) -> str: return text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
