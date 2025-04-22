import { useState, useEffect } from "react";

interface Square {
  id: number;
  top: string;
  left: string;
  xMove: number;
  yMove: number;
  animationDuration: string;
  animationDelay: string;
  backgroundColor: string;
}

const Background: React.FC = () => {
  const [squares, setSquares] = useState<Square[]>([]);

  const createSquares = () => {
    const numSquares = 15;
    const newSquares: Square[] = [];

    for (let i = 0; i < numSquares; i++) {
      // Ensure that random movement stays within reasonable limits
      const randomX = Math.random() * 20 - 10; // Moves between -10vw and 10vw
      const randomY = Math.random() * 20 - 10; // Moves between -10vh and 10vh
      const randomDuration = Math.random() * 15 + 10;
      const randomDelay = Math.random() * 5;

      newSquares.push({
        id: i,
        // Set initial positions within the bounds of the viewport
        top: `${Math.random() * 90}vh`,
        left: `${Math.random() * 90}vw`,
        xMove: randomX,
        yMove: randomY,
        animationDuration: `${randomDuration}s`,
        animationDelay: `${randomDelay}s`,
        backgroundColor: `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.5)`,
      });
    }
    setSquares(newSquares);
  };

  useEffect(() => {
    createSquares();
  }, []);

  useEffect(() => {
    const styleSheet = document.styleSheets[0];
    if (styleSheet) {
      squares.forEach((square) => {
        const keyframes = `
          @keyframes moveSquare-${square.id} {
            0% {
              transform: translate(0, 0);
            }
            25% {
              transform: translate(${square.xMove}vw, ${square.yMove}vh);
            }
            50% {
              transform: translate(${square.xMove * 0.5}vw, ${square.yMove * 0.5}vh);
            }
            75% {
              transform: translate(${square.xMove}vw, ${square.yMove}vh);
            }
            100% {
              transform: translate(0, 0);
            }
          }
        `;
        styleSheet.insertRule(keyframes, styleSheet.cssRules.length);
      });
    }
  }, [squares]);

  return (
    <div id="square-container" className="absolute w-full h-full z-0 top-0 left-0">
      {squares.map((square) => (
        <div
          key={square.id}
          className="square"
          style={{
            position: "absolute",
            top: square.top,
            left: square.left,
            animation: `moveSquare-${square.id} ${square.animationDuration} ease-in-out ${square.animationDelay} infinite`,
            backgroundColor: square.backgroundColor,
            width: "20px",
            height: "20px",
            borderRadius: "4px",
          }}
        ></div>
      ))}
    </div>
  );
};

export default Background;
