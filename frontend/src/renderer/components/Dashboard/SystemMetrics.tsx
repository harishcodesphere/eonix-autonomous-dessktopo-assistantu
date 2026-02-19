import { useSystemStore } from '../../store/systemStore'
import { formatBytes } from '../../utils/formatters'

export function SystemMetrics() {
    const { stats } = useSystemStore()

    if (!stats) return <div className="text-gray-500">Loading metrics...</div>

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-4">
            <MetricCard
                label="CPU Usage"
                value={`${stats.cpu.percent}%`}
                subtext={`${stats.cpu.cores} Cores`}
                color="text-cyan-400"
                barColor="bg-cyan-400"
                percent={stats.cpu.percent}
            />
            <MetricCard
                label="Memory"
                value={`${stats.memory.percent}%`}
                subtext={`${stats.memory.used_gb}/${stats.memory.total_gb} GB`}
                color="text-purple-400"
                barColor="bg-purple-400"
                percent={stats.memory.percent}
            />
            <MetricCard
                label="Disk Status"
                value={`${stats.disk.percent}%`}
                subtext={`${stats.disk.used_gb} GB Used`}
                color="text-emerald-400"
                barColor="bg-emerald-400"
                percent={stats.disk.percent}
            />
            {stats.battery && (
                <MetricCard
                    label="Battery"
                    value={`${stats.battery.percent}%`}
                    subtext={stats.battery.plugged ? '⚡ Charging' : '🔋 On Battery'}
                    color={stats.battery.percent < 20 ? 'text-red-400' : 'text-yellow-400'}
                    barColor={stats.battery.percent < 20 ? 'bg-red-400' : 'bg-yellow-400'}
                    percent={stats.battery.percent}
                />
            )}
        </div>
    )
}

function MetricCard({ label, value, subtext, color, barColor, percent }: any) {
    return (
        <div className="bg-gray-800/40 backdrop-blur-md border border-gray-700/50 rounded-xl p-4 shadow-lg hover:bg-gray-800/60 transition-colors">
            <div className="flex justify-between items-start mb-2">
                <span className="text-gray-400 text-xs font-semibold uppercase tracking-wider">{label}</span>
            </div>
            <div className={`text-2xl font-mono font-bold mb-1 ${color}`}>{value}</div>
            <div className="text-xs text-gray-500 mb-3">{subtext}</div>
            <div className="w-full h-1 bg-gray-700 rounded-full overflow-hidden">
                <div
                    className={`h-full rounded-full transition-all duration-500 ${barColor}`}
                    style={{ width: `${percent}%` }}
                />
            </div>
        </div>
    )
}
