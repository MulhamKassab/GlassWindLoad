export default function InputField({ label, id, value, onChange, required = false, submitted = false, ...rest }) {
  const hasError = submitted && required && !value;
  const isValid = submitted && value;

  const inputClass = hasError
    ? 'input-error'
    : isValid
    ? 'input-success'
    : '';

  return (
    <div className="form-group">
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        type="number"
        value={value}
        onChange={e => onChange(e.target.value)}
        className={inputClass}
        {...rest}
      />
    </div>
  );
}
