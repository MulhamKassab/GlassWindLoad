import { useState } from 'react';
import Spinner from '../components/Spinner';
import LayerGroup from '../components/LayerGroup';
import ResultsPanel from '../components/ResultsPanel';
import InputField from '../components/InputField';
import SelectField from '../components/SelectField';
import { calculate } from '../api/api';

const emptyLayer = () => ({
  layerType: '',
  thickness: '',
  strength: '',
  plies: []
});


export default function CalculatorPage() {
  const [form, setForm] = useState({
    shortLoad: '',
    longLoad: '',
    allowableDef: '',
    length: '',
    width: '',
    supportedSides: '',
    glazing: '',
    layers: [{ layerType: '', thickness: '', strength: '', plies: [] }]
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const updateLayer = (i, layer) => {
    const updated = [...form.layers];
    updated[i] = layer;
    setForm({ ...form, layers: updated });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitted(true); // trigger validation
  
    setError('');
    setLoading(true);
    try {
      const payload = mapToBackend(form);
      const res = await calculate(payload);
      setResult(res);
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <div className="container">
      <div className="logo-container">
        <img
          src={`${process.env.PUBLIC_URL}/logo.png`}
          alt="Gutmann Logo"
          className="company-logo"
        />
      </div>
  
      <h1>Glass Wind Load Calculator</h1>
  
      <form onSubmit={handleSubmit} className="form">
        <div className="form-container">
          {/* LEFT COLUMN */}
          <div className="column">
            <div className="form-group">
              <InputField label="Short Duration Load (kPa)" id="shortLoad" value={form.shortLoad} onChange={v => setForm({ ...form, shortLoad: v })} required submitted={submitted} />
            </div>
  
            <div className="form-group">
              <InputField label="Long Duration Load (kPa)" id="longLoad" value={form.longLoad} onChange={v => setForm({ ...form, longLoad: v })} />
            </div>
  
            <div className="form-group">
              <InputField label="Allowable Deflection (mm)" id="allowableDef" value={form.allowableDef} onChange={v => setForm({ ...form, allowableDef: v })} required submitted={submitted} />
            </div>
  
            <div className="form-group">
              <SelectField
                label="Number of Supported Sides"
                id="supportedSides"
                value={form.supportedSides}
                onChange={v => setForm({ ...form, supportedSides: v })}
                options={[
                  { value: '', label: 'Choose' },
                  { value: 1, label: '1' },
                  { value: 2, label: '2' },
                  { value: 4, label: '4' },
                ]}
                required
                submitted={submitted}
              />
            </div>
  
            <div className="form-group">
              <InputField label="Glass Length (mm)" id="length" value={form.length} onChange={v => setForm({ ...form, length: v })} required submitted={submitted}/>
            </div>
  
            {form.supportedSides !== '1' && (
              <div className="form-group">
                <InputField label="Glass Width (mm)" id="width" value={form.width} onChange={v => setForm({ ...form, width: v })} required submitted={submitted}/>
              </div>
            )}
  
            <div className="form-group">
              <SelectField
                label="Glazing Type"
                id="glazing"
                value={form.glazing}
                onChange={v => {
                  const layers = v === 'double' ? [emptyLayer(), emptyLayer()] : [emptyLayer()];
                  setForm({ ...form, glazing: v, layers });
                }}
                options={[
                  { value: '', label: 'Choose' },
                  { value: 'single', label: 'Single Glazed' },
                  { value: 'double', label: 'Double Glazed' },
                ]}
                required
                submitted={submitted}
              />
            </div>
          </div>
  
          {/* RIGHT COLUMN - LAYERS */}
          <div className="column">
            {form.layers.map((layer, i) => (
              <LayerGroup
              key={i}
              idx={i}
              layer={layer}
              glazingType={form.glazing}
              updateLayer={updateLayer}
              submitted={submitted}
            />
            
            ))}
          </div>
        </div>
  
        <button type="submit" className="btn">Calculate</button>
      </form>
  
      {loading && <Spinner />}
      {error && <p className="error-message">{error}</p>}
      <ResultsPanel result={result} />
    </div>
  );
  
}

function mapToBackend(f) {
  const layersTypes = f.layers.map(l => l.layerType || 'mono');
  const layersThicknesses = f.layers.map(l => Number(l.thickness || 0));
  const glassLayersStrengthType = f.layers.map(l => l.strength || '');
  const pvbThicknesses = f.layers.flatMap(l => l.plies?.slice(0, -1).map(p => p.interlayerThick || 0) || []);
  const interlayerTypes = f.layers.flatMap(l => l.plies?.slice(0, -1).map(p => p.interlayerType || 'PVB') || []);

  return {
    data: {
      shortDurationLoad: Number(f.shortLoad || 0),
      longDurationLoad: Number(f.longLoad || 0),
      allowable_Deflection: Number(f.allowableDef || 0),
      glassLength: Number(f.length || 0),
      glassWidth: Number(f.width || 0),
      numberOfSupportedSides: Number(f.supportedSides || 0),
      glazingType: f.glazing,
      numberOfLayers: f.layers.length,
      layersTypes,
      layersThicknesses,
      glassLayersStrengthType,
      pvbThicknesses,
      interlayerTypes
    },
    plyThicknessList: f.layers.flatMap(l => l.plies?.map(p => p.thickness) || [])
  };
}