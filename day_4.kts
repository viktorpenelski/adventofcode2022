import java.nio.file.Files
import java.nio.file.Paths
import java.util.stream.Collectors


data class Range(val start: Int, val end: Int) {
    fun fullyOverlaps(other: Range): Boolean {
        return this.start <= other.start && this.end >= other.end
    }
    fun overlaps(other: Range): Boolean {
        return other.start <= this.start && this.start <= other.end
    }
}

val input: List<String> = Files.lines(Paths.get("inputs/day_4.txt")).collect(Collectors.toList())
val rangePairs = input.map { it.split(',') }
    .map { it.map { sections -> sections.split('-') } }
    .map<List<List<String>>, List<Range>> { it.map { pair -> Range(start=pair[0].toInt(), end = pair[1].toInt()) } }

val partOne = rangePairs
    .filter { it[0].fullyOverlaps(it[1]) || it[1].fullyOverlaps(it[0]) }
    .count()
println(partOne)

val partTwo = rangePairs
    .filter { it[0].overlaps(it[1]) || it[1].overlaps(it[0])  }
    .count()
println(partTwo)