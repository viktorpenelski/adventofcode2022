import java.nio.file.Files
import java.nio.file.Paths
import java.time.LocalDateTime
import java.util.stream.Collectors
import java.util.stream.IntStream
import kotlin.math.abs
import kotlin.math.max
import kotlin.system.measureTimeMillis

data class Point(val x: Int, val y: Int) {
    fun manhattanDistanceTo(pt: Point): Int = abs(this.x - pt.x) + abs(this.y - pt.y)
}

data class RangeIncl(val from: Int, val to: Int, val y: Int = -1)

val input: List<Pair<Point, Point>> = Files
    .lines(Paths.get("D:\\dev\\aoc2022\\inputs\\day_15.txt"))
    .filter { it != null }
    .map { parseRow(it) }
    .collect(Collectors.toList())

fun parseRow(row: String): Pair<Point, Point> {
    val s = row.substringAfter("Sensor at ").split(":")[0].split(",")
    val sensor = Point(s[0].split("=")[1].toInt(), s[1].split("=")[1].toInt())
    val b = row.split(" closest beacon is at ")[1].split(",")
    val beacon = Point(b[0].split("=")[1].toInt(), b[1].split("=")[1].toInt())
    return Pair(sensor, beacon)
}

fun List<RangeIncl>.converge(y: Int): List<RangeIncl> {
    if (this.size <= 1) {
        return this
    }
    val sorted = this.sortedWith(compareBy({it.from}, {it.to}))
    val newRanges = mutableListOf<RangeIncl>()
    var left = sorted[0].from
    var right = sorted[0].to
    for (i in 1 until sorted.size) {
        val nextLeft = sorted[i].from
        val nextRight = sorted[i].to
        if (right + 1 < nextLeft) {
            newRanges.add(RangeIncl(left, right, y))
            left = nextLeft
            right = nextRight
        } else {
            right = max(right, nextRight)
        }
    }
    newRanges.add(RangeIncl(left, right, y))
    return newRanges.toList()
}

fun blockedRangeFrom(y: Int, sensor: Point, beacon: Point): RangeIncl? {
    val distToBeacon = sensor.manhattanDistanceTo(beacon)
    val closestPtY = Point(sensor.x, y)
    val distToClosestPtY = sensor.manhattanDistanceTo(closestPtY)
    if (distToClosestPtY <= distToBeacon) {
        val leftoverDist: Int = distToBeacon - distToClosestPtY
        return RangeIncl(sensor.x - leftoverDist, sensor.x + leftoverDist, y)
    }
    return null
}

fun blockedRanges(y: Int, sensorBeaconPairs: List<Pair<Point, Point>>): List<RangeIncl> {
    return sensorBeaconPairs
        .mapNotNull { blockedRangeFrom(y, it.first, it.second) }
        .converge(y)
}

fun solvePt2(max_y: Int) {
    IntStream.range(0, max_y + 1)
        .parallel()
        .mapToObj { blockedRanges(it, input) }
        .filter { it.size == 2 }
        .findFirst()
        .also {
            it.ifPresent { ranges ->
                val x: Long = max(ranges[0].from, ranges[1].from).toLong() - 1
                println(4_000_000 * x + ranges[0].y)
            }
        }
}

val timeMs = measureTimeMillis {
    solvePt2(4000000)
}
println("execution took $timeMs ms.")
