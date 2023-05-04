USE uniDB;
SELECT s.name, a.name, c.title
FROM Student s
JOIN attend d ON s.StuNo = d.StuNo
JOIN Course c ON d.CouNo = c.CouNo
JOIN Assistant a ON a.boss = c.TaugthBy;