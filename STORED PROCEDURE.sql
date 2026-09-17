--USE STUDENT_QUERY;
--CREATE PROCEDURE GetStudentDetail
--@FirstName VARCHAR(50)
--AS
--BEGIN 
--SELECT * FROM STUDENT
--WHERE First_Name=@FirstName;
--END;
EXEC GetStudentDetail @FirstName='S.A.JENISHA';
EXEC GetStudentDetail @Firstname='T';