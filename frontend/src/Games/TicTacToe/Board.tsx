import styled from "@emotion/styled";

interface BoardProps {
  board: string[][];
  onClick: (x: number, y: number) => void;
  disabled: boolean;
}

export const Board = (props: BoardProps) => (
  <BoardContainer>
    {props.board.map((row, i) => (
      <RowContainer key={i}>
        {row.map((cell, j) => (
          <Cell
            key={j}
            onClick={() => props.onClick(i, j)}
            disabled={props.disabled || cell !== ""}
            selectable={!props.disabled && cell === ""}
          >
            {cell}
          </Cell>
        ))}
      </RowContainer>
    ))}
  </BoardContainer>
);

const BoardContainer = styled.div({
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  justifyContent: "center",
  width: "100%",
  height: "100%",
  margin: "20px",
});

const RowContainer = styled.div({
  display: "flex",
  flexDirection: "row",
  alignItems: "center",
  justifyContent: "center",
  width: "100%",
  height: "100%",
});

const Cell = styled.button<{selectable: boolean}>((props) => ({
  width: "50px",
  height: "50px",
  fontSize: "24px",
  border: "1px solid black",
  cursor: "pointer",
  backgroundColor: "white",
  "&:hover": {
    backgroundColor: props.selectable ? "lightgray" : "white",
  },
}));