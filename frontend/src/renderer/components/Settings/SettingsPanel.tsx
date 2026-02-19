export function SettingsPanel() {
    return (
        <div className="p-8 max-w-2xl mx-auto">
            <h2 className="text-2xl font-light mb-8">Settings</h2>

            <div className="space-y-6">
                <SettingSection title="General">
                    <Toggle label="Launch on Startup" checked={true} />
                    <Toggle label="Always on Top" checked={false} />
                </SettingSection>

                <SettingSection title="Voice">
                    <Input label="Wake Word" value="Hey Eonix" />
                    <Select label="Voice Model" options={['Amy (English)', 'Ryan (English)']} />
                </SettingSection>

                <SettingSection title="AI Model">
                    <Input label="Ollama Host" value="http://localhost:11434" />
                    <Select label="Model" options={['llama3', 'mistral', 'neural-chat']} />
                </SettingSection>
            </div>
        </div>
    )
}

function SettingSection({ title, children }: any) {
    return (
        <div className="bg-gray-800/40 backdrop-blur-md border border-gray-700/50 rounded-xl p-6">
            <h3 className="text-lg font-medium text-gray-300 mb-4">{title}</h3>
            <div className="space-y-4">{children}</div>
        </div>
    )
}

function Toggle({ label, checked }: any) {
    return (
        <div className="flex items-center justify-between">
            <span className="text-gray-400">{label}</span>
            <div className={`w-10 h-6 rounded-full p-1 cursor-pointer transition-colors ${checked ? 'bg-cyan-500' : 'bg-gray-700'}`}>
                <div className={`w-4 h-4 bg-white rounded-full shadow-md transform transition-transform ${checked ? 'translate-x-4' : ''}`} />
            </div>
        </div>
    )
}

function Input({ label, value }: any) {
    return (
        <div className="space-y-2">
            <label className="text-sm text-gray-500">{label}</label>
            <input type="text" defaultValue={value} className="w-full bg-gray-900/50 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-cyan-500 transition-colors" />
        </div>
    )
}

function Select({ label, options }: any) {
    return (
        <div className="space-y-2">
            <label className="text-sm text-gray-500">{label}</label>
            <select className="w-full bg-gray-900/50 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-cyan-500 transition-colors">
                {options.map((opt: string) => <option key={opt}>{opt}</option>)}
            </select>
        </div>
    )
}
