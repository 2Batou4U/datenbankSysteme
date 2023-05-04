USE uniDB;
SELECT s.name, a.name, c.title
FROM Student s, attend d, Assistant a, Course c
WHERE s.StuNo = d.StuNo
AND d.CouNo=c.CouNo
AND a.boss = c.TaugthBy;