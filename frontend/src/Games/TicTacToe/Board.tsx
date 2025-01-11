import styled from "@emotion/styled";

interface BoardProps {
  board: string[][];
  onClick: (x: number, y: number) => void;
}

export const Board = (props: BoardProps) => (
  <div>
    {props.board.map((row, i) => (
      <div key={i}>
        {row.map((cell, j) => (
          <Cell key={j} onClick={() => props.onClick(i, j)}>{cell}</Cell>
        ))}
      </div>
    ))}
  </div>
);

const Cell = styled.button({
  width: "50px",
  height: "50px",
  fontSize: "24px",
  border: "1px solid black",
  cursor: "pointer",
  backgroundColor: "white",
  "&:hover": {
    backgroundColor: "lightgray",
  },
});