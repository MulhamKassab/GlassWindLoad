import { useEffect } from 'react';
import SelectField from './SelectField';
import InputField from './InputField';

const plyOpts = [2.5, 2.7, 3, 4, 5, 6, 8, 10].map(v => ({ value: v, label: v.toFixed(1) }));
const interlayerOpts = [{ value: 'PVB', label: 'PVB' }, { value: 'SGP', label: 'SGP' }];
const pvbThickOpts = [0.381, 0.762, 1.143, 1.524, 1.905, 2.286].map(v => ({ value: v, label: v.toFixed(3) }));

export default function LayerPlyInputs({ idx, layer, updateLayer, submitted = false }) {
  const fixedPlies = 2;

  // Ensure exactly 2 plies always exist
  useEffect(() => {
    if (!layer.plies || layer.plies.length !== fixedPlies) {
      const defaultPlies = Array.from({ length: fixedPlies }, () => ({
        thickness: '',
        interlayerType: 'PVB',
        interlayerThick: ''
      }));
      updateLayer(idx, { ...layer, plies: defaultPlies });
    }
  }, [layer.plies]);

  const updatePly = (pIndex, newPly) => {
    const newPlies = [...layer.plies];
    newPlies[pIndex] = newPly;
    updateLayer(idx, { ...layer, plies: newPlies });
  };

  return (
    <div>
      <p><strong>Number of Plies: 2 (fixed)</strong></p>

      {layer.plies?.map((ply, pIdx) => (
        <div key={pIdx} className="border p-2 rounded mb-2 bg-white">
          <SelectField
            label={`Ply ${pIdx + 1} Thickness (mm)`}
            id={`plyThickness${idx}-${pIdx}`}
            value={ply.thickness}
            onChange={val => updatePly(pIdx, { ...ply, thickness: parseFloat(val) })}
            options={[{ value: '', label: 'Select' }, ...plyOpts]}
            required
            submitted={submitted}
          />

          {pIdx === 0 && (
            <>
              <SelectField
                label="Interlayer type"
                id={`interlayerType${idx}-${pIdx}`}
                value={ply.interlayerType}
                onChange={val => updatePly(pIdx, { ...ply, interlayerType: val })}
                options={interlayerOpts}
                required
                submitted={submitted}
              />

              <SelectField
                label="Interlayer thickness (mm)"
                id={`interlayerThickness${idx}-${pIdx}`}
                value={ply.interlayerThick}
                onChange={val => updatePly(pIdx, { ...ply, interlayerThick: parseFloat(val) })}
                options={[{ value: '', label: 'Select' }, ...pvbThickOpts]}
                required
                submitted={submitted}
              />
            </>
          )}
        </div>
      ))}
    </div>
  );
}
