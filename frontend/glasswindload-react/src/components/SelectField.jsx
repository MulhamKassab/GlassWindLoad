export default function SelectField({ label, id, value, onChange, required = false, submitted = false, options }) {
  const hasError = submitted && required && !value;
  const isValid = submitted && value;

  const selectClass = hasError
    ? 'input-error'
    : isValid
    ? 'input-success'
    : '';

  return (
    <div className="form-group">
      <label htmlFor={id}>{label}</label>
      <select
        id={id}
        value={value}
        onChange={e => onChange(e.target.value)}
        className={selectClass}
      >
        {options.map(({ value, label }) => (
          <option key={value ?? 'blank'} value={value ?? ''}>
            {label}
          </option>
        ))}
      </select>
    </div>
  );
}
