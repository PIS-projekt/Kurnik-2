// eslint-disable-next-line
const copyToClipboard = (val: any) => {
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(val);
  } else {
    // copy using execcommand api
    const value = val;
    const input = document.createElement("input");
    input.value = value;
    document.body.appendChild(input);
    input.select();
    document.execCommand("copy");
    document.body.removeChild(input);
  }
};

export default copyToClipboard;
