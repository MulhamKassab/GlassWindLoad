import SelectField from './SelectField';
import InputField from './InputField';
import LayerPlyInputs from './LayerPlyInputs';

export default function LayerGroup({ idx, layer, updateLayer, glazingType, submitted }) {
  const onTypeChange = (v) => updateLayer(idx, { ...layer, layerType: v, plies: [] });
  const onThickness = (v) => updateLayer(idx, { ...layer, thickness: parseFloat(v) });
  const onStrength = (v) => updateLayer(idx, { ...layer, strength: v });

  const thicknessOpts = [2.5, 3, 4, 5, 6, 8, 10, 12, 16, 19].map(v => ({ value: v, label: v.toFixed(1) }));

  return (
    <div className="form-group">
      <SelectField
        label={glazingType === 'single' ? 'Single Glazed Layer Type' : `Glass Type of Layer ${idx + 1}`}
        id={`layerType${idx}`}
        value={layer.layerType}
        onChange={onTypeChange}
        options={[
          { value: '', label: 'Select' },
          { value: 'mono', label: 'Monolithic' },
          { value: 'laminated', label: 'Laminated' }
        ]}
      />

      {layer.layerType === 'mono' && (
        <>
          <SelectField
            label={`Layer ${idx + 1} Thickness (mm)`}
            id={`monoThickness${idx}`}
            value={layer.thickness}
            onChange={onThickness}
            options={[{ value: '', label: 'Select' }, ...thicknessOpts]}
          />
          <SelectField
            label={`Glass Strength of Layer ${idx + 1}`}
            id={`strength${idx}`}
            value={layer.strength}
            onChange={onStrength}
            options={[
              { value: '', label: 'Select' },
              { value: 'annealed', label: 'Annealed' },
              { value: 'heatStrengthened', label: 'Heat Strengthened' },
              { value: 'tempered', label: 'Tempered' }
            ]}
          />
        </>
      )}

      {layer.layerType === 'laminated' && (
        <LayerPlyInputs idx={idx} layer={layer} updateLayer={updateLayer} submitted={submitted} />
      )}
    </div>
  );
}
