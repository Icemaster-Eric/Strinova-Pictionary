const drawDisplay = document.getElementById("draw-display");
drawDisplay.width = ((window.innerHeight * 4) / 3) * devicePixelRatio;
drawDisplay.height = window.innerHeight * devicePixelRatio;
/** @type {CanvasRenderingContext2D} */
const ctx = drawDisplay.getContext("2d");

const drawCommands = [];
let isDrawing = false;
const POINTERDOWN = 0;
const POINTERMOVED = 1;
ctx.strokeStyle = "red";
ctx.lineCap = "round";
ctx.lineJoin = "round";
ctx.lineWidth = 5;
let prevPoint = [];

const toCanvasRelativePos = (x, y) => [
	(x - drawDisplay.offsetLeft + window.scrollX) * devicePixelRatio,
	(y - drawDisplay.offsetTop + window.scrollY) * devicePixelRatio,
];
drawDisplay.addEventListener("pointerdown", (ev) => {
	let [cvsX, cvsY] = toCanvasRelativePos(ev.x, ev.y);
	isDrawing = true;
	ctx.beginPath();
	ctx.moveTo(cvsX, cvsY);
	prevPoint = [cvsX, cvsY];
});
drawDisplay.addEventListener("pointermove", (ev) => {
	let [cvsX, cvsY] = toCanvasRelativePos(ev.x, ev.y);
	if (!isDrawing) return;
	ctx.quadraticCurveTo(
		cvsX,
		cvsY,
		(prevPoint[0] + cvsX) / 2,
		(prevPoint[1] + cvsY) / 2
	);
	ctx.stroke();
	prevPoint = [cvsX, cvsY];
});
drawDisplay.addEventListener("pointerup", () => {
	isDrawing = false;
});
