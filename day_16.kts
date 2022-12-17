import java.nio.file.Files
import java.nio.file.Paths
import java.util.Comparator
import kotlin.math.min
import kotlin.system.measureTimeMillis


data class Valve(val name: String, val flowRate: Int, val connections: Set<String>) {
    companion object {
        val allValves: MutableMap<String, Valve> = mutableMapOf()

        fun fromInputLine(line: String): Valve {
            val name = line.substring(6, 8)
            val flowRate = line.split('=', ';')[1].toInt()
            val nodes = if (line.contains("valves")) {
                line.split("tunnels lead to valves ")[1].split(", ")
            } else {
                listOf(line.split(" tunnel leads to valve ")[1])
            }
            val valve = Valve(name, flowRate, nodes.toSet())
            allValves[name] = valve
            return valve
        }
    }
}

Files.lines(Paths.get("inputs/day_16.txt"))
    .forEach {
        Valve.fromInputLine(it)
    }


fun shortestPath(from: Valve, to: Valve, mapped: MutableMap<String, Int>, visited: Set<String>): Int {
    // CACHING OF SHAME
//    if ("${from.name}->${to.name}" in mapped && mapped["${from.name}->${to.name}"] != 9999) {
//        return mapped["${from.name}->${to.name}"]!!
//    }
    if (from == to) {
        return 0
    }
    if (to.name in from.connections) {
        mapped["${from.name}->${to.name}"] = 1
        mapped["${to.name}->${from.name}"] = 1
        return 1
    }
    val newVisited = visited.plus(from.name)
    var minDist = 9999
    for (connection in from.connections) {
        val childNode = Valve.allValves[connection]!!
        if (!newVisited.contains(connection)) {
            minDist = min(minDist, 1 + shortestPath(childNode, to, mapped, newVisited))
        }
    }
    if (!mapped.contains("${from.name}->${to.name}") || minDist < mapped["${from.name}->${to.name}"]!!) {
        mapped["${from.name}->${to.name}"] = minDist
        mapped["${to.name}->${from.name}"] = minDist
    }
    return minDist
}

fun shortestPaths(): Map<String, Int> {
    val mapped = Valve.allValves.values.associate {
        Pair("${it.name}->${it.name}", 0)
    }.toMutableMap()
    for (from in Valve.allValves.values) {
        for (to in Valve.allValves.values) {
            shortestPath(from, to, mapped, mutableSetOf())
        }
    }
    return mapped

}

fun pressure(
    valve: Valve,
    released: Set<Valve>,
    paths: Map<String, Int>,
    pressureValves: Set<Valve>,
    timeLeft: Int,
    allPaths: MutableList<Pair<Set<Valve>, Int>>,
    totalPressure: Int,
) {
    if (timeLeft <= 0) {
        return
    }
    val localTime = timeLeft - 1
    val releasedAfter = released.plus(valve)
    val localPressure = valve.flowRate * localTime
    allPaths.add(Pair(releasedAfter, totalPressure + localPressure))
    for (v in pressureValves.minus(releasedAfter)) {
        pressure(v, releasedAfter, paths, pressureValves, localTime - paths["${valve.name}->${v.name}"]!!, allPaths, totalPressure + localPressure)
    }
}

fun solvePt1() {
    val nodesWithFlow = Valve.allValves.values.filter { it.flowRate > 0 }.toSet()
    val shortestPaths = shortestPaths()
    val allPaths: MutableList<Pair<Set<Valve>, Int>> = mutableListOf()
    for (node in nodesWithFlow) {
        pressure(
            node,
            setOf(),
            shortestPaths,
            nodesWithFlow,
            30 - shortestPaths["AA->${node.name}"]!!,
            allPaths,
            0,
        )
    }
    println(allPaths.maxOf { it.second })
}

fun solvePt2() {
    val nodesWithFlow = Valve.allValves.values.filter { it.flowRate > 0 }.toSet()
    val shortestPaths = shortestPaths()
    val allPaths: MutableList<Pair<Set<Valve>, Int>> = mutableListOf()
    for (node in nodesWithFlow) {
        pressure(
            node,
            setOf(),
            shortestPaths,
            nodesWithFlow,
            26 - shortestPaths["AA->${node.name}"]!!,
            allPaths,
            0,
        )
    }
    val maxPressure = allPaths
        .parallelStream()
        .map { p1 ->
            allPaths.map { p2 ->
                if (!p1.first.any(p2.first::contains)) {
                    p1.second + p2.second
                } else {
                    null
                }
            }.filterNotNull()
        }.flatMap { it.stream() }.max(Comparator.naturalOrder())
    println(maxPressure)
}


val ms1 = measureTimeMillis {
    solvePt1()
}
println("pt1 execution took $ms1 ms.")

val ms2 = measureTimeMillis {
    solvePt2()
}
println("pt2 execution took $ms2 ms.")
