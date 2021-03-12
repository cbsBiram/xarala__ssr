import redis
from django.conf import settings
from course.models import Course


# connect to redis
r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


class Recommender(object):
    def get_course_key(self, id):
        return f"course:{id}:purchased_with"

    def products_bought(self, courses):
        course_ids = [p.id for p in courses]
        for course_id in course_ids:
            for with_id in course_ids:
                # get the other courses bought with each course
                if course_id != with_id:
                    # increment score for course purchased together
                    r.zincrby(self.get_course_key(course_id), 1, with_id)

    def suggest_products_for(self, courses, max_results=6):
        course_ids = [course.id for course in courses]
        if len(courses) == 1:
            # only 1 course
            suggestions = r.zrange(
                self.get_course_key(course_ids[0]), 0, -1, desc=True
            )[:max_results]
        else:
            # generate a temporary key
            flat_ids = "".join([str(id) for id in course_ids])
            tmp_key = f"tmp_{flat_ids}"
            # multiple courses, combine scores of all courses
            # store the resulting sorted set in a temporary key
            keys = [self.get_course_key(id) for id in course_ids]
            r.zunionstore(tmp_key, keys)
            # remove ids for the courses the recommendation is for
            r.zrem(tmp_key, *course_ids)
            # get the course ids by their score, descendant sort
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # remove the temporary key
            r.delete(tmp_key)
        suggested_courses_ids = [int(id) for id in suggestions]

        # get suggested courses and sort by order of appearance
        suggested_courses = list(Course.objects.filter(id__in=suggested_courses_ids))
        suggested_courses.sort(key=lambda x: suggested_courses_ids.index(x.id))
        return suggested_courses

    def clear_purchases(self):
        for id in Course.objects.values_list("id", flat=True):
            r.delete(self.get_course_key(id))
